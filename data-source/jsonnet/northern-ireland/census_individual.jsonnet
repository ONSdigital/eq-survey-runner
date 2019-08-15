// personal details
local accommodation_type = import 'blocks/individual/personal-details/accommodation_type.jsonnet';
local confirm_dob = import 'blocks/individual/personal-details/confirm_dob.jsonnet';
local date_of_birth = import 'blocks/individual/personal-details/date_of_birth.jsonnet';
local establishment_position = import 'blocks/individual/personal-details/establishment_position.jsonnet';
local in_education = import 'blocks/individual/personal-details/in_education.jsonnet';
local marriage_type = import 'blocks/individual/personal-details/marriage_type.jsonnet';
local name = import 'blocks/individual/personal-details/name.jsonnet';
local proxy = import 'blocks/individual/personal-details/proxy.jsonnet';
local sex = import 'blocks/individual/personal-details/sex.jsonnet';
local term_time_location = import 'blocks/individual/personal-details/term_time_location.jsonnet';

// identity and health
local arrive_in_country = import 'blocks/individual/identity-and-health/arrive_in_country.jsonnet';
local carer = import 'blocks/individual/identity-and-health/carer.jsonnet';
local country_of_birth = import 'blocks/individual/identity-and-health/country_of_birth.jsonnet';
local disability = import 'blocks/individual/identity-and-health/disability.jsonnet';
local disability_limitation = import 'blocks/individual/identity-and-health/disability_limitation.jsonnet';
local disability_other = import 'blocks/individual/identity-and-health/disability_other.jsonnet';
local ethnic_group = import 'blocks/individual/identity-and-health/ethnic_group.jsonnet';
local frequency_irish = import 'blocks/individual/identity-and-health/frequency_irish.jsonnet';
local frequency_ulster_scots = import 'blocks/individual/identity-and-health/frequency_ulster_scots.jsonnet';
local health = import 'blocks/individual/identity-and-health/health.jsonnet';
local language = import 'blocks/individual/identity-and-health/language.jsonnet';
local last_year_address = import 'blocks/individual/identity-and-health/last_year_address.jsonnet';
local national_identity = import 'blocks/individual/identity-and-health/national_identity.jsonnet';
local no_religion = import 'blocks/individual/identity-and-health/no_religion.jsonnet';
local passports = import 'blocks/individual/identity-and-health/passports.jsonnet';
local past_usual_household_address = import 'blocks/individual/identity-and-health/past_usual_household_address.jsonnet';
local religion = import 'blocks/individual/identity-and-health/religion.jsonnet';
local sexual_identity = import 'blocks/individual/identity-and-health/sexual_identity.jsonnet';
local speak_english = import 'blocks/individual/identity-and-health/speak_english.jsonnet';
local understand_irish = import 'blocks/individual/identity-and-health/understand_irish.jsonnet';
local understand_ulster_scots = import 'blocks/individual/identity-and-health/understand_ulster_scots.jsonnet';

// school
local school_location = import 'blocks/individual/school/school_location.jsonnet';
local school_travel = import 'blocks/individual/school/school_travel.jsonnet';

// qualifications
local a_level = import 'blocks/individual/qualifications/a_level.jsonnet';
local apprenticeship = import 'blocks/individual/qualifications/apprenticeship.jsonnet';
local degree = import 'blocks/individual/qualifications/degree.jsonnet';
local gcse = import 'blocks/individual/qualifications/gcse.jsonnet';
local nvq_level = import 'blocks/individual/qualifications/nvq_level.jsonnet';
local other_qualifications = import 'blocks/individual/qualifications/other_qualifications.jsonnet';
local qualifications = import 'blocks/individual/qualifications/qualifications.jsonnet';

// employment
local armed_forces = import 'blocks/individual/employment/armed_forces.jsonnet';
local business_name = import 'blocks/individual/employment/business_name.jsonnet';
local employer_address_depot = import 'blocks/individual/employment/employer_address_depot.jsonnet';
local employer_address_workplace = import 'blocks/individual/employment/employer_address_workplace.jsonnet';
local employer_type_of_address = import 'blocks/individual/employment/employer_type_of_address.jsonnet';
local employers_business = import 'blocks/individual/employment/employers_business.jsonnet';
local employment_status = import 'blocks/individual/employment/employment_status.jsonnet';
local employment_type = import 'blocks/individual/employment/employment_type.jsonnet';
local ever_worked = import 'blocks/individual/employment/ever_worked.jsonnet';
local hours_worked = import 'blocks/individual/employment/hours_worked.jsonnet';
local job_availability = import 'blocks/individual/employment/job_availability.jsonnet';
local job_description = import 'blocks/individual/employment/job_description.jsonnet';
local job_pending = import 'blocks/individual/employment/job_pending.jsonnet';
local job_title = import 'blocks/individual/employment/job_title.jsonnet';
local jobseeker = import 'blocks/individual/employment/jobseeker.jsonnet';
local main_employment_block = import 'blocks/individual/employment/main_employment_block.jsonnet';
local main_job_type = import 'blocks/individual/employment/main_job_type.jsonnet';
local supervise = import 'blocks/individual/employment/supervise.jsonnet';
local work_location = import 'blocks/individual/employment/work_location.jsonnet';
local work_travel = import 'blocks/individual/employment/work_travel.jsonnet';

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
            work_location,
            work_travel,
          ],
        },
        {
          id: 'school-group',
          title: 'School',
          blocks: [
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
