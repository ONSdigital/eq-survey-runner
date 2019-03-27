def make_schema(data_version, section, group, block, question):
    return {
        'survey_id': '021',
        'data_version': data_version,
        'sections': [
            {
                'id': section,
                'groups': [
                    {
                        'id': group,
                        'blocks': [
                            {
                                'id': block,
                                'question': question
                            }
                        ]
                    }
                ]
            }
        ]
    }
