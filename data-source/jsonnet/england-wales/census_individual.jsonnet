// personal details
local accommodation_type = import 'individual/blocks/personal-details/accommodation_type.jsonnet';
local address_type = import 'individual/blocks/personal-details/address_type.jsonnet';
local another_address = import 'individual/blocks/personal-details/another_address.jsonnet';
local confirm_dob = import 'individual/blocks/personal-details/confirm_dob.jsonnet';
local current_marriage_status = import 'individual/blocks/personal-details/current_marriage_status.jsonnet';
local current_partnership_status = import 'individual/blocks/personal-details/current_partnership_status.jsonnet';
local date_of_birth = import 'individual/blocks/personal-details/date_of_birth.jsonnet';
local establishment_position = import 'individual/blocks/personal-details/establishment_position.jsonnet';
local in_education = import 'individual/blocks/personal-details/in_education.jsonnet';
local marriage_type = import 'individual/blocks/personal-details/marriage_type.jsonnet';
local name = import 'individual/blocks/personal-details/name.jsonnet';
local other_uk_address = import 'individual/blocks/personal-details/other_uk_address.jsonnet';
local previous_marriage_status = import 'individual/blocks/personal-details/previous_marriage_status.jsonnet';
local previous_partnership_status = import 'individual/blocks/personal-details/previous_partnership_status.jsonnet';
local proxy = import 'individual/blocks/personal-details/proxy.jsonnet';
local sex = import 'individual/blocks/personal-details/sex.jsonnet';
local term_time_address_country = import 'individual/blocks/personal-details/term_time_address_country.jsonnet';
local term_time_address_details = import 'individual/blocks/personal-details/term_time_address_details.jsonnet';
local term_time_location = import 'individual/blocks/personal-details/term_time_location.jsonnet';

// Identity and Health
local arrive_in_country = import 'individual/blocks/identity-and-health/arrive_in_country.jsonnet';
local birth_gender = import 'individual/blocks/identity-and-health/birth_gender.jsonnet';
local carer = import 'individual/blocks/identity-and-health/carer.jsonnet';
local country_of_birth = import 'individual/blocks/identity-and-health/country_of_birth.jsonnet';
local disability = import 'individual/blocks/identity-and-health/disability.jsonnet';
local disability_limitation = import 'individual/blocks/identity-and-health/disability_limitation.jsonnet';
local ethnic_group = import 'individual/blocks/identity-and-health/ethnic_group.jsonnet';
local ethnic_group_asian = import 'individual/blocks/identity-and-health/ethnic_group_asian.jsonnet';
local ethnic_group_black = import 'individual/blocks/identity-and-health/ethnic_group_black.jsonnet';
local ethnic_group_mixed = import 'individual/blocks/identity-and-health/ethnic_group_mixed.jsonnet';
local ethnic_group_other = import 'individual/blocks/identity-and-health/ethnic_group_other.jsonnet';
local ethnic_group_white = import 'individual/blocks/identity-and-health/ethnic_group_white.jsonnet';
local health = import 'individual/blocks/identity-and-health/health.jsonnet';
local language = import 'individual/blocks/identity-and-health/language.jsonnet';
local last_year_address = import 'individual/blocks/identity-and-health/last_year_address.jsonnet';
local length_of_stay = import 'individual/blocks/identity-and-health/length_of_stay.jsonnet';
local national_identity = import 'individual/blocks/identity-and-health/national_identity.jsonnet';
local passports = import 'individual/blocks/identity-and-health/passports.jsonnet';
local past_usual_household_address = import 'individual/blocks/identity-and-health/past_usual_household_address.jsonnet';
local religion = import 'individual/blocks/identity-and-health/religion.jsonnet';
local sexual_identity = import 'individual/blocks/identity-and-health/sexual_identity.jsonnet';
local speak_english = import 'individual/blocks/identity-and-health/speak_english.jsonnet';
local understand_welsh = import 'individual/blocks/identity-and-health/understand_welsh.jsonnet';
local when_arrive_in_uk = import 'individual/blocks/identity-and-health/when_arrive_in_uk.jsonnet';

// Qualifications
local a_level = import 'individual/blocks/qualifications/a_level.jsonnet';
local apprenticeship = import 'individual/blocks/qualifications/apprenticeship.jsonnet';
local degree = import 'individual/blocks/qualifications/degree.jsonnet';
local gcse = import 'individual/blocks/qualifications/gcse.jsonnet';
local nvq_level = import 'individual/blocks/qualifications/nvq_level.jsonnet';
local other_qualifications = import 'individual/blocks/qualifications/other_qualifications.jsonnet';
local qualifications = import 'individual/blocks/qualifications/qualifications.jsonnet';

// employment
local armed_forces = import 'individual/blocks/employment/armed_forces.jsonnet';
local business_name = import 'individual/blocks/employment/business_name.jsonnet';
local employer_address_depot = import 'individual/blocks/employment/employer_address_depot.jsonnet';
local employer_address_workplace = import 'individual/blocks/employment/employer_address_workplace.jsonnet';
local employer_type_of_address = import 'individual/blocks/employment/employer_type_of_address.jsonnet';
local employers_business = import 'individual/blocks/employment/employers_business.jsonnet';
local employment_status = import 'individual/blocks/employment/employment_status.jsonnet';
local employment_type = import 'individual/blocks/employment/employment_type.jsonnet';
local ever_worked = import 'individual/blocks/employment/ever_worked.jsonnet';
local hours_worked = import 'individual/blocks/employment/hours_worked.jsonnet';
local job_availability = import 'individual/blocks/employment/job_availability.jsonnet';
local job_description = import 'individual/blocks/employment/job_description.jsonnet';
local job_pending = import 'individual/blocks/employment/job_pending.jsonnet';
local job_title = import 'individual/blocks/employment/job_title.jsonnet';
local jobseeker = import 'individual/blocks/employment/jobseeker.jsonnet';
local main_employment_block = import 'individual/blocks/employment/main_employment_block.jsonnet';
local main_job_type = import 'individual/blocks/employment/main_job_type.jsonnet';
local supervise = import 'individual/blocks/employment/supervise.jsonnet';
local work_travel = import 'individual/blocks/employment/work_travel.jsonnet';

local understandWelshBlock(region_code) = if region_code == 'GB-WLS' then [understand_welsh] else [];

function(region_code, census_date, census_month_year_date) {
  mime_type: 'application/json/ons/eq',
  schema_version: '0.0.1',
  data_version: '0.0.3',
  survey_id: 'census',
  title: '2019 Census Test',
  description: 'Census England Individual Schema',
  theme: 'census',
  legal_basis: 'Voluntary',
  navigation: {
    visible: false,
  },
  metadata: [
    {
      name: 'user_id',
      type: 'string',
    },
    {
      name: 'period_id',
      type: 'string',
    },
    {
      name: 'display_address',
      type: 'string',
    },
  ],
  sections: [
    {
      id: 'individual-section',
      title: 'Individual Section',
      groups: [
        {
          id: 'personal-details-group',
          title: 'Personal Details',
          blocks: [
            accommodation_type,
            proxy,
            name,
            establishment_position,
            date_of_birth(census_date),
            confirm_dob,
            sex,
            marriage_type(census_date),
            current_marriage_status,
            previous_marriage_status,
            current_partnership_status,
            previous_partnership_status,
            another_address,
            other_uk_address,
            address_type,
            in_education,
            term_time_location,
            term_time_address_country,
            term_time_address_details,
          ],
        },
        {
          id: 'identity-and-health-group',
          title: 'Identity and Health',
          blocks: [
            country_of_birth(region_code),
            arrive_in_country(region_code, census_month_year_date),
            when_arrive_in_uk(region_code),
            length_of_stay(region_code),
          ] + understandWelshBlock(region_code) + [
            language(region_code),
            speak_english,
            national_identity(region_code),
            ethnic_group(region_code),
            ethnic_group_white(region_code),
            ethnic_group_mixed,
            ethnic_group_asian,
            ethnic_group_black,
            ethnic_group_other,
            religion(region_code),
            past_usual_household_address,
            last_year_address,
            passports,
            health,
            disability,
            disability_limitation,
            carer,
            sexual_identity,
            birth_gender,
          ],
        },
        {
          id: 'qualifications-group',
          title: 'Qualifications',
          blocks: [
            qualifications(region_code),
            apprenticeship(region_code),
            degree(region_code),
            nvq_level(region_code),
            a_level(region_code),
            gcse(region_code),
            other_qualifications(region_code),
          ],
        },
        {
          id: 'employment-group',
          title: 'Employment',
          blocks: [
            armed_forces,
            employment_status,
            employment_type,
            jobseeker,
            job_availability,
            job_pending,
            ever_worked,
            main_employment_block,
            main_job_type,
            business_name,
            job_title,
            job_description,
            employers_business(region_code),
            supervise,
            hours_worked,
            work_travel,
            employer_type_of_address,
            employer_address_workplace,
            employer_address_depot,
          ],
        },
      ],
    },
    {
      id: 'submit-answers-section',
      title: 'Submit answers',
      groups: [
        {
          id: 'submit-group',
          title: 'Submit answers',
          blocks: [
            {
              id: 'summary',
              type: 'Summary',
            },
          ],
        },
      ],
    },
  ],
}
