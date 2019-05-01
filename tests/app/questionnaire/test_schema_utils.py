from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.schema_utils import choose_question_to_display, choose_content_to_display, transform_variants

def compare_transformed_block(base_block, transformed_block, title):
    assert transformed_block != base_block
    assert 'question_variants' not in transformed_block
    assert transformed_block['question']['title'] == title

def test_transform_variants_with_question_variants(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    answer_store = AnswerStore({})
    answer_store.add_or_update(Answer(answer_id='when-answer', value='no'))
    metadata = {}

    block = schema.get_block('block1')

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    compare_transformed_block(block, transformed_block, 'Question 1, No')

    answer_store.add_or_update(Answer(answer_id='when-answer', value='yes'))

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    compare_transformed_block(block, transformed_block, 'Question 1, Yes')

def test_transform_variants_with_content(content_variant_schema):
    schema = QuestionnaireSchema(content_variant_schema)
    answer_store = AnswerStore({})
    answer_store.add_or_update(Answer(answer_id='age-answer', value='18'))
    metadata = {}

    block = schema.get_block('block1')

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    assert transformed_block != block
    assert 'content_variants' not in transformed_block
    assert transformed_block['content'][0]['title'] == 'You are over 16'

def test_transform_variants_with_no_variants(question_schema):
    schema = QuestionnaireSchema(question_schema)
    answer_store = AnswerStore({})
    metadata = {}

    block = schema.get_block('block1')

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    assert transformed_block == block

def test_transform_variants_list_collector(list_collector_variant_schema):
    schema = QuestionnaireSchema(list_collector_variant_schema)
    answer_store = AnswerStore({})
    answer_store.add_or_update(Answer(answer_id='when-answer', value='no'))
    metadata = {}

    block = schema.get_block('block1')

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    compare_transformed_block(block['add_block'], transformed_block['add_block'], 'Add, No')
    compare_transformed_block(block['remove_block'], transformed_block['remove_block'], 'Remove, No')
    compare_transformed_block(block['edit_block'], transformed_block['edit_block'], 'Edit, No')

    answer_store.add_or_update(Answer(answer_id='when-answer', value='yes'))

    transformed_block = transform_variants(block, schema, metadata, answer_store)

    compare_transformed_block(block['add_block'], transformed_block['add_block'], 'Add, Yes')
    compare_transformed_block(block['remove_block'], transformed_block['remove_block'], 'Remove, Yes')
    compare_transformed_block(block['edit_block'], transformed_block['edit_block'], 'Edit, Yes')

def test_choose_content_to_display(content_variant_schema):
    schema = QuestionnaireSchema(content_variant_schema)
    answer_store = AnswerStore({})
    answer_store.add_or_update(Answer(answer_id='age-answer', value='18'))
    metadata = {}

    content_to_display = choose_content_to_display(schema.get_block('block1'), schema, metadata, answer_store)

    assert content_to_display[0]['title'] == 'You are over 16'

    answer_store = AnswerStore({})

    content_to_display = choose_content_to_display(schema.get_block('block1'), schema, metadata, answer_store)

    assert content_to_display[0]['title'] == 'You are ageless'

def test_choose_question_to_display(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    answer_store = AnswerStore({})
    answer_store.add_or_update(Answer(answer_id='when-answer', value='yes'))
    metadata = {}

    question_to_display = choose_question_to_display(schema.get_block('block1'), schema, metadata, answer_store)

    assert question_to_display['title'] == 'Question 1, Yes'

    answer_store = AnswerStore({})

    question_to_display = choose_question_to_display(schema.get_block('block1'), schema, metadata, answer_store)

    assert question_to_display['title'] == 'Question 1, No'
