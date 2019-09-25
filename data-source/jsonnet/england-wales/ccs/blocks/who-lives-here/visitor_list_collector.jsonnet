local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local questionTitle(census_date) = {
  text: 'Were there any other visitors staying overnight on {census_date} at {address}?',
  placeholders: [
    placeholders.censusDate(census_date),
    placeholders.address,
  ],
};

local summaryTitle(census_date) = {
  text: 'Visitors staying overnight on {census_date}',
  placeholders: [
    placeholders.censusDate(census_date),
  ],
};

local summaryTitlePersonName = {
  text: '{person_name}',
  placeholders: [
    placeholders.personName,
  ],
};

local visitorGuidance = {
  contents: [
    {
      title: 'Include',
    },
    {
      list: [
        'People staying here because it is their second address, for example, for work. Their permanent or family home is elsewhere',
        'People here on holiday',
      ],
    },
  ],
};

local addVisitorQuestionTitle(census_date) = {
  text: 'What is the name of the visitor staying overnight on {census_date} at {address}?',
  placeholders: [
    placeholders.censusDate(census_date),
    placeholders.address,
  ],
};

local editPersonQuestionTitle = {
  text: 'Change details for {person_name}',
  placeholders: [
    placeholders.personName,
  ],
};

local removePersonQuestionTitle = {
  text: 'Are you sure you want to remove {person_name}?',
  placeholders: [
    placeholders.personName,
  ],
};


function(census_date) {
  id: 'visitor-list-collector',
  type: 'ListCollector',
  for_list: 'visitor',
  add_answer: {
    id: 'visitor-answer',
    value: 'Yes, I need to add someone',
  },
  remove_answer: {
    id: 'visitor-remove-confirmation',
    value: 'Yes, I want to remove this person',
  },
  question: {
    id: 'visitor-confirmation-question',
    type: 'General',
    title: questionTitle(census_date),
    guidance: visitorGuidance,
    answers: [
      {
        id: 'visitor-answer',
        mandatory: true,
        type: 'Radio',
        options: [
          {
            label: 'Yes, I need to add someone',
            value: 'Yes, I need to add someone',
          },
          {
            label: 'No, I do not need to add anyone',
            value: 'No, I do not need to add anyone',
          },
        ],
      },
    ],
  },
  add_block: {
    id: 'add-visitor',
    type: 'ListAddQuestion',
    question: {
      id: 'visitor-add-question',
      type: 'General',
      title: addVisitorQuestionTitle(census_date),
      guidance: visitorGuidance,
      answers: [
        {
          id: 'first-name',
          label: 'First name',
          mandatory: true,
          type: 'TextField',
        },
        {
          id: 'last-name',
          label: 'Last name',
          mandatory: true,
          type: 'TextField',
        },
      ],
    },
  },
  edit_block: {
    id: 'edit-visitor',
    type: 'ListEditQuestion',
    question: {
      id: 'visitor-edit-question',
      type: 'General',
      title: editPersonQuestionTitle,
      answers: [
        {
          id: 'first-name',
          label: 'First name',
          mandatory: true,
          type: 'TextField',
        },
        {
          id: 'last-name',
          label: 'Last name',
          mandatory: true,
          type: 'TextField',
        },
      ],
    },
  },
  remove_block: {
    id: 'remove-visitor',
    type: 'ListRemoveQuestion',
    question: {
      id: 'visitor-remove-question',
      type: 'General',
      guidance: {
        contents: [{
          title: 'All of the data entered about this person will be deleted',
        }],
      },
      title: removePersonQuestionTitle,
      answers: [
        {
          id: 'visitor-remove-confirmation',
          mandatory: true,
          type: 'Radio',
          options: [
            {
              label: 'Yes, I want to remove this person',
              value: 'Yes, I want to remove this person',
            },
            {
              label: 'No, I do not want to remove this person',
              value: 'No, I do not want to remove this person',
            },
          ],
        },
      ],
    },
  },
  summary: {
    title: summaryTitle(census_date),
    item_title: summaryTitlePersonName,
    add_link_text: 'Add a visitor',
    empty_list_text: 'There are no visitors',
  },
  show_on_section_summary: true,
}
