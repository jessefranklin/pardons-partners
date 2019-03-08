from flask import render_template, make_response
from flask_restful import Resource
import traceback
from time import time

from models.confirmation import ConfirmationModel
from schemas.confirmation import ConfirmationSchema
from models.user import UserModel
from libs.mailgun import MailGunException

confirmation_schema = ConfirmationSchema()

class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": "Not found"}, 404

        if confirmation.expired:
            return {"message": "Expired"}, 400

        if confirmation.confirmed:
            return {"message": "Already confirmed"}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers,
        )


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{'Messafe':'Usewr Not found'}, 404

        return (
            {
                "current_time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            }, 200,
        )

    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{'Messafe':'Usewr Not found'}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {'message': 'already confrimated'}, 400
                confirmation.forced_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {'message': 'Resend successful'}, 200
        except MailGunException as e :
            return {'message': str(e)}, 500
        except:
            traceback.print_exc()
            return {'message': 'Resend fail'}, 500
