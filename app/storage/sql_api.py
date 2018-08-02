from sqlalchemy.exc import IntegrityError

from app.data_model import app_models, models
from app.storage.errors import ItemAlreadyExistsError


TABLE_CONFIG = {
    app_models.QuestionnaireState: {
        'key_field': 'user_id',
        'sql_model': models.QuestionnaireState,
    },
    app_models.EQSession: {
        'key_field': 'eq_session_id',
        'sql_model': models.EQSession,
    },
    app_models.UsedJtiClaim: {
        'key_field': 'jti_claim',
        'sql_model': models.UsedJtiClaim,
    },
}


def get_by_key(model_type, key_value):
    config = TABLE_CONFIG[model_type]
    key = {config['key_field']: key_value}
    returned_data = config['sql_model'].query.filter_by(**key).first()
    if returned_data:
        return returned_data.to_app_model()


def put(model, overwrite):
    config = TABLE_CONFIG[type(model)]
    sql_model = config['sql_model'].from_app_model(model)

    try:
        # pylint: disable=maybe-no-member
        if overwrite:
            models.db.session.merge(sql_model)
        else:
            models.db.session.add(sql_model)

        models.db.session.commit()
    except IntegrityError as e:
        raise ItemAlreadyExistsError() from e


def delete(model):
    config = TABLE_CONFIG[type(model)]
    sql_model = config['sql_model'].from_app_model(model)

    # pylint: disable=maybe-no-member
    sql_model = models.db.session.merge(sql_model)
    models.db.session.delete(sql_model)
    models.db.session.commit()
