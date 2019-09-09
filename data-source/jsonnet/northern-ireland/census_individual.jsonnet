// Personal Details
local accommodation_type = import 'individual/blocks/personal-details/accommodation_type.jsonnet';
local confirm_dob = import 'individual/blocks/personal-details/confirm_dob.jsonnet';
local date_of_birth = import 'individual/blocks/personal-details/date_of_birth.jsonnet';
local establishment_position = import 'individual/blocks/personal-details/establishment_position.jsonnet';
local in_education = import 'individual/blocks/personal-details/in_education.jsonnet';
local marriage_type = import 'individual/blocks/personal-details/marriage_type.jsonnet';
local name = import 'individual/blocks/personal-details/name.jsonnet';
local proxy = import 'individual/blocks/personal-details/proxy.jsonnet';
local sex = import 'individual/blocks/personal-details/sex.jsonnet';
local term_time_location = import 'individual/blocks/personal-details/term_time_location.jsonnet';

// Identity and Health
local arrive_in_country = import 'individual/blocks/identity-and-health/arrive_in_country.jsonnet';
local carer = import 'individual/blocks/identity-and-health/carer.jsonnet';
local country_of_birth = import 'individual/blocks/identity-and-health/country_of_birth.jsonnet';
local disability = import 'individual/blocks/identity-and-health/disability.jsonnet';
local disability_limitation = import 'individual/blocks/identity-and-health/disability_limitation.jsonnet';
local disability_other = import 'individual/blocks/identity-and-health/disability_other.jsonnet';
local ethnic_group = import 'individual/blocks/identity-and-health/ethnic_group.jsonnet';
local frequency_irish = import 'individual/blocks/identity-and-health/frequency_irish.jsonnet';
local frequency_ulster_scots = import 'individual/blocks/identity-and-health/frequency_ulster_scots.jsonnet';
local health = import 'individual/blocks/identity-and-health/health.jsonnet';
local language = import 'individual/blocks/identity-and-health/language.jsonnet';
local last_year_address = import 'individual/blocks/identity-and-health/last_year_address.jsonnet';
local national_identity = import 'individual/blocks/identity-and-health/national_identity.jsonnet';
local no_religion = import 'individual/blocks/identity-and-health/no_religion.jsonnet';
local passports = import 'individual/blocks/identity-and-health/passports.jsonnet';
local past_usual_household_address = import 'individual/blocks/identity-and-health/past_usual_household_address.jsonnet';
local religion = import 'individual/blocks/identity-and-health/religion.jsonnet';
local sexual_identity = import 'individual/blocks/identity-and-health/sexual_identity.jsonnet';
local speak_english = import 'individual/blocks/identity-and-health/speak_english.jsonnet';
local understand_irish = import 'individual/blocks/identity-and-health/understand_irish.jsonnet';
local understand_ulster_scots = import 'individual/blocks/identity-and-health/understand_ulster_scots.jsonnet';

// School
local school_location = import 'individual/blocks/school/school_location.jsonnet';
local school_travel = import 'individual/blocks/school/school_travel.jsonnet';
local study_location_type = import 'individual/blocks/school/study_location_type.jsonnet';

// Qualifications
local a_level = import 'individual/blocks/qualifications/a_level.jsonnet';
local apprenticeship = import 'individual/blocks/qualifications/apprenticeship.jsonnet';
local degree = import 'individual/blocks/qualifications/degree.jsonnet';
local gcse = import 'individual/blocks/qualifications/gcse.jsonnet';
local nvq_level = import 'individual/blocks/qualifications/nvq_level.jsonnet';
local other_qualifications = import 'individual/blocks/qualifications/other_qualifications.jsonnet';
local qualifications = import 'individual/blocks/qualifications/qualifications.jsonnet';

// Employment
local armed_forces = import 'individual/blocks/employment/armed_forces.jsonnet';
local business_name = import 'individual/blocks/employment/business_name.jsonnet';
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
local work_location = import 'individual/blocks/employment/work_location.jsonnet';
local work_location_type = import 'individual/blocks/employment/work_location_type.jsonnet';
local work_travel = import 'individual/blocks/employment/work_travel.jsonnet';

function(region_code, census_date) {
  mime_type: 'application/json/ons/eq',
  schema_version: '0.0.1',
  data_version: '0.0.3',
  survey_id: 'census',
  title: '2019 Census Test',
  description: 'Census England Individual Schema',
  theme: 'census-nisra',
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
            marriage_type,
            in_education,
            term_time_location,
          ],
        },
        {
          id: 'identity-and-health-group',
          title: 'Identity and Health',
          blocks: [
            country_of_birth,
            arrive_in_country,
            past_usual_household_address,
            last_year_address,
            passports,
            national_identity,
            ethnic_group,
            religion,
            no_religion,
            language,
            speak_english,
            understand_irish,
            frequency_irish,
            understand_ulster_scots,
            frequency_ulster_scots,
            health,
            disability_limitation,
            disability,
            disability_other,
            carer,
            sexual_identity,
          ],
        },
        {
          id: 'qualifications-group',
          title: 'Qualifications',
          blocks: [
            qualifications,
            degree,
            gcse,
            a_level,
            nvq_level,
            other_qualifications,
            apprenticeship,
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
            employers_business,
            supervise,
            hours_worked,
            work_location_type,
            work_location,
            work_travel,
          ],
        },
        {
          id: 'school-group',
          title: 'School',
          blocks: [
            study_location_type,
            school_location,
            school_travel,
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
