// personal details
local accommodation_type = import '../common/blocks/individual/personal-details/accommodation_type.jsonnet';
local confirm_dob = import '../common/blocks/individual/personal-details/confirm_dob.jsonnet';
local date_of_birth = import '../common/blocks/individual/personal-details/date_of_birth.jsonnet';
local establishment_position = import '../common/blocks/individual/personal-details/establishment_position.jsonnet';
local in_education = import '../common/blocks/individual/personal-details/in_education.jsonnet';
local name = import '../common/blocks/individual/personal-details/name.jsonnet';
local proxy = import '../common/blocks/individual/personal-details/proxy.jsonnet';
local marriage_type = import 'blocks/individual/personal-details/marriage_type.jsonnet';
local sex = import 'blocks/individual/personal-details/sex.jsonnet';
local term_time_location = import 'blocks/individual/personal-details/term_time_location.jsonnet';

// identity and health
local health = import '../common/blocks/individual/identity-and-health/health.jsonnet';
local last_year_address = import '../common/blocks/individual/identity-and-health/last_year_address.jsonnet';
local passports = import '../common/blocks/individual/identity-and-health/passports.jsonnet';
local speak_english = import '../common/blocks/individual/identity-and-health/speak_english.jsonnet';
local arrive_in_country = import 'blocks/individual/identity-and-health/arrive_in_country.jsonnet';
local carer = import 'blocks/individual/identity-and-health/carer.jsonnet';
local country_of_birth = import 'blocks/individual/identity-and-health/country_of_birth.jsonnet';
local disability = import 'blocks/individual/identity-and-health/disability.jsonnet';
local disability_limitation = import 'blocks/individual/identity-and-health/disability_limitation.jsonnet';
local disability_other = import 'blocks/individual/identity-and-health/disability_other.jsonnet';
local ethnic_group = import 'blocks/individual/identity-and-health/ethnic_group.jsonnet';
local frequency_irish = import 'blocks/individual/identity-and-health/frequency_irish.jsonnet';
local frequency_ulster_scots = import 'blocks/individual/identity-and-health/frequency_ulster_scots.jsonnet';
local language = import 'blocks/individual/identity-and-health/language.jsonnet';
local national_identity = import 'blocks/individual/identity-and-health/national_identity.jsonnet';
local no_religion = import 'blocks/individual/identity-and-health/no_religion.jsonnet';
local past_usual_household_address = import 'blocks/individual/identity-and-health/past_usual_household_address.jsonnet';
local religion = import 'blocks/individual/identity-and-health/religion.jsonnet';
local sexual_identity = import 'blocks/individual/identity-and-health/sexual_identity.jsonnet';
local understand_irish = import 'blocks/individual/identity-and-health/understand_irish.jsonnet';
local understand_ulster_scots = import 'blocks/individual/identity-and-health/understand_ulster_scots.jsonnet';

// school
local school_location = import 'blocks/individual/school/school_location.jsonnet';
local school_travel_mode = import 'blocks/individual/school/school_travel_mode.jsonnet';

// qualifications
local a_level = import 'blocks/individual/qualifications/a_level.jsonnet';
local apprenticeship = import 'blocks/individual/qualifications/apprenticeship.jsonnet';
local degree = import 'blocks/individual/qualifications/degree.jsonnet';
local gcse = import 'blocks/individual/qualifications/gcse.jsonnet';
local nvq_level = import 'blocks/individual/qualifications/nvq_level.jsonnet';
local other_qualifications = import 'blocks/individual/qualifications/other_qualifications.jsonnet';
local qualifications = import 'blocks/individual/qualifications/qualifications.jsonnet';

// employment
local business_name = import '../common/blocks/individual/employment/business_name.jsonnet';
local employer_address_depot = import '../common/blocks/individual/employment/employer_address_depot.jsonnet';
local employer_address_workplace = import '../common/blocks/individual/employment/employer_address_workplace.jsonnet';
local employment_status = import '../common/blocks/individual/employment/employment_status.jsonnet';
local employment_type = import '../common/blocks/individual/employment/employment_type.jsonnet';
local hours_worked = import '../common/blocks/individual/employment/hours_worked.jsonnet';
local job_availability = import '../common/blocks/individual/employment/job_availability.jsonnet';
local job_description = import '../common/blocks/individual/employment/job_description.jsonnet';
local job_pending = import '../common/blocks/individual/employment/job_pending.jsonnet';
local job_title = import '../common/blocks/individual/employment/job_title.jsonnet';
local jobseeker = import '../common/blocks/individual/employment/jobseeker.jsonnet';
local main_employment_block = import '../common/blocks/individual/employment/main_employment_block.jsonnet';
local main_job_type = import '../common/blocks/individual/employment/main_job_type.jsonnet';
local supervise = import '../common/blocks/individual/employment/supervise.jsonnet';
local work_travel = import '../common/blocks/individual/employment/work_travel.jsonnet';
local armed_forces = import 'blocks/individual/employment/armed_forces.jsonnet';
local employer_type_of_address = import 'blocks/individual/employment/employer_type_of_address.jsonnet';
local employers_business = import 'blocks/individual/employment/employers_business.jsonnet';
local ever_worked = import 'blocks/individual/employment/ever_worked.jsonnet';

function(region_code, census_date) {
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
      name: 'case_type',
      type: 'string',
      optional: true,
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
            nvq_level,
            a_level,
            gcse,
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
            work_travel,
            employer_type_of_address,
            employer_address_workplace,
            employer_address_depot,
          ],
        },
        {
          id: 'school-group',
          title: 'School',
          blocks: [
            school_location,
            school_travel_mode,
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
