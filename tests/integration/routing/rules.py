CHOOSE_A_SIDE_LIGHT_SIDE = [
    {
        'block_id': 'choose-your-side-block',
        'answers': [
            {
                'answer': 'Which side of the force are you on',
                'answer_id': 'choose-your-side-answer',
                'user_answer': 'Light Side'
            }
        ],
        'destination_id': 'light-side-pick-character-ship'
    }]

CHOOSE_A_SIDE_DARK_SIDE = [
    {
        'block_id': 'choose-your-side-block',
        'answers': [
            {
                'answer': 'Which side of the force are you on',
                'answer_id': 'choose-your-side-answer',
                'user_answer': 'Dark Side'
            }
        ],
        'destination_id': 'dark-side-pick-character-ship'
    }]

CHOOSE_A_SIDE_STAR_TREK = [
    {
        'block_id': 'choose-your-side-block',
        'answers': [
            {
                'answer': 'Which side of the force are you on',
                'answer_id': 'choose-your-side-answer',
                'user_answer': 'I prefer Star Trek'
            }
        ],
        'destination_id': 'summary'
    }]

LIGHT_SHIP_YES = [
    {
        'block_id': 'light-side-pick-character-ship',
        'answers': [
            {
                'answer': 'Do you want to pick a ship?',
                'answer_id': 'light-side-pick-ship-answer',
                'user_answer': 'Yes'
            },
            {
                'answer': 'A wise choice young Jedi. Pick your hero',
                'answer_id': 'light-side-pick-character-answer',
                'user_answer': 'Dan Skywalker'
            }
        ],
        'destination_id': 'light-side-ship-type'
    }]

LIGHT_SHIP_NO = [
    {
        'block_id': 'light-side-pick-character-ship',
        'answers': [
            {
                'answer': 'Do you want to pick a ship?',
                'answer_id': 'light-side-pick-ship-answer',
                'user_answer': 'No'
            },
            {
                'answer': 'A wise choice young Jedi. Pick your hero',
                'answer_id': 'light-side-pick-character-answer',
                'user_answer': 'Leyoda'
            }
        ],
        'destination_id': 'star-wars-trivia'
    }]

LIGHT_SHIP_PICK = [
    {
        'block_id': 'light-side-ship-type',
        'answers': [
            {
                'answer': 'Which ship do you want?',
                'answer_id': 'light-side-ship-type-answer',
                'user_answer': 'X-wing'
            }
        ],
        'destination_id': 'star-wars-trivia'
    }]

DARK_SHIP_YES = [
    {
        'block_id': 'dark-side-pick-character-ship',
        'answers': [
            {
                'answer': 'Do you want to pick a ship?',
                'answer_id': 'dark-side-pick-ship-answer',
                'user_answer': 'Yes'
            },
            {
                'answer': 'Good! Your hate has made you powerful. Pick your baddie',
                'answer_id': 'dark-side-pick-character-answer',
                'user_answer': 'Darth Vadan'
            }
        ],
        'destination_id': 'dark-side-ship-type'
    }]

DARK_SHIP_NO = [
    {
        'block_id': 'dark-side-pick-character-ship',
        'answers': [
            {
                'answer': 'Do you want to pick a ship?',
                'answer_id': 'dark-side-pick-ship-answer',
                'user_answer': 'No'
            },
            {
                'answer': 'Good! Your hate has made you powerful. Pick your baddie',
                'answer_id': 'dark-side-pick-character-answer',
                'user_answer': 'Boba Fetewis'
            }
        ],
        'destination_id': 'star-wars-trivia'
    }]

DARK_SHIP_PAIN = [
    {
        'block_id': 'dark-side-pick-character-ship',
        'answers': [
            {
                'answer': 'Do you want to pick a ship?',
                'answer_id': 'dark-side-pick-ship-answer',
                'user_answer': 'Can I be a pain and have a goodies ship'
            },
            {
                'answer': 'Good! Your hate has made you powerful. Pick your baddie',
                'answer_id': 'dark-side-pick-character-answer',
                'user_answer': 'Jabba the Hutarren'
            }
        ],
        'destination_id': 'light-side-ship-type'
    }]

DARK_SHIP_PICK = [
    {
        'block_id': 'dark-side-ship-type',
        'answers': [
            {
                'answer': 'Which ship do you want?',
                'answer_id': 'dark-side-ship-type-answer',
                'user_answer': 'Death Star'
            }
        ],
        'destination_id': 'star-wars-trivia'
    }]

QUIZ_PAGE_1 = [
    {
        'block_id': 'star-wars-trivia',
        'answers': [
            {
                'answer': 'How old is Chewy?',
                'answer_id': 'chewies-age-answer',
                'user_answer': '234'
            },
            {
                'answer': 'How many Octillions do Nasa reckon it would cost to build a death star?',
                'answer_id': 'death-star-cost-answer',
                'user_answer': '40'
            },
            {
                'answer': 'How hot is a lightsaber in degrees C?',
                'answer_id': 'lightsaber-cost-answer',
                'user_answer': '1370'
            },
            {
                'answer': 'What animal was used to create the engine sound of the Empire',
                'answer_id': 'tie-fighter-sound-answer',
                'user_answer': 'Elephant'
            },
            {
                'answer': 'Which of these Darth Vader quotes is wrong?',
                'answer_id': 'darth-vader-quotes-answer',
                'user_answer': 'Luke, I am your father'
            },
            {
                'answer': 'Which 3 have wielded a green lightsaber?',
                'answer_id': 'green-lightsaber-answer',
                'user_answer': 'Yoda'
            },
            {
                'answer': 'When was The Empire Strikes Back released?',
                'answer_id': 'empire-strikes-back-from-answer-day',
                'user_answer': '28'
            },
            {
                'answer': 'When was The Empire Strikes Back released?',
                'answer_id': 'empire-strikes-back-from-answer-month',
                'user_answer': '5'
            },
            {
                'answer': 'When was The Empire Strikes Back released?',
                'answer_id': 'empire-strikes-back-from-answer-year',
                'user_answer': '1983'
            },
            {
                'answer': 'When was The Empire Strikes Back released?',
                'answer_id': 'empire-strikes-back-to-answer-day',
                'user_answer': '29'
            },
            {
                'answer': 'When was The Empire Strikes Back released?',
                'answer_id': 'empire-strikes-back-to-answer-month',
                'user_answer': '5'
            },
            {
                'answer': 'When was The Empire Strikes Back released?',
                'answer_id': 'empire-strikes-back-to-answer-year',
                'user_answer': '1983'
            }
        ],
        'destination_id': 'star-wars-trivia-part-2'
    }
]

QUIZ_PAGE_2 = [
    {
        'block_id': 'star-wars-trivia-part-2',
        'answers': [
            {
                'answer': 'Chewbacca receive a medal at the end of A New Hope?',
                'answer_id': 'chewbacca-medal-answer',
                'user_answer': 'Wookiees don’t place value in material rewards and refused the medal initially'
            },
            {
                'answer': 'Do you really think that Chewbacca is 234 years old?',
                'answer_id': 'confirm-chewbacca-age-answer',
                'user_answer': 'Yes'
            },
            {
                'answer': 'What do you think of the prequel series?',
                'answer_id': 'star-wars-prequel-answer',
                'user_answer': 'Awesome, I love them all'
            }
        ],
        'destination_id': 'star-wars-trivia-part-3'
    }
]

QUIZ_PAGE_3 = [
    {
        'block_id': 'star-wars-trivia-part-3',
        'answers': [
            {
                'answer': 'What is the name of Jar Jar Binks',
                'answer_id': 'jar-jar-binks-planet-answer',
                'user_answer': 'Naboo'
            }
        ],
        'destination_id': 'summary'
    }
]
