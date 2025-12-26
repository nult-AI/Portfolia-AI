/**
 * Transform frontend data structure to API format
 */
export const transformToApiFormat = {
  profile: (data) => ({
    name: data.name,
    role: data.role,
    bio: data.bio,
    email: data.email,
    phone: data.phone,
    location: data.location,
    skype: data.skype,
    linkedin_url: data.linkedin,
    github_url: data.github,
    profile_image_url: data.profileImage,
  }),

  experience: (data) => ({
    company_name: data.company,
    role: data.role,
    period_display: data.period,
    tech_stack: data.techStack,
    duties: data.duties || [],
    domains: data.domain || [],
  }),

  education: (data) => ({
    school: data.school,
    degree: data.degree,
    major: data.major,
    education_year: data.year,
  }),

  skillCategory: (categoryName, skills, displayOrder = 0) => ({
    name: categoryName,
    display_order: displayOrder,
  }),

  skill: (name, categoryId) => ({
    name,
    category_id: categoryId,
  }),

  otherSkill: (name) => ({
    name,
  }),
};

/**
 * Transform API response to frontend format
 */
export const transformFromApiFormat = {
  profile: (data) => ({
    id: data.id,
    name: data.name,
    role: data.role,
    bio: data.bio,
    email: data.email,
    phone: data.phone,
    location: data.location,
    skype: data.skype,
    linkedin: data.linkedin_url,
    github: data.github_url,
    profileImage: data.profile_image_url,
  }),

  experience: (data) => ({
    id: data.id,
    company: data.company_name,
    role: data.role,
    period: data.period_display,
    techStack: data.tech_stack,
    duties: data.duties?.map(d => d.description) || [],
    domain: data.domains?.map(d => d.name) || [],
  }),

  education: (data) => ({
    id: data.id,
    school: data.school,
    degree: data.degree,
    major: data.major,
    year: data.education_year,
  }),

  skillsByCategory: (categories) => {
    const result = {};
    categories.forEach(cat => {
      result[cat.name] = cat.skills.map(s => s.name);
    });
    return result;
  },

  otherSkills: (skills) => skills.map(s => ({ id: s.id, name: s.name })),
};
