-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS experience_duties CASCADE;
DROP TABLE IF EXISTS experience_domains CASCADE;
DROP TABLE IF EXISTS experiences CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS skill_categories CASCADE;
DROP TABLE IF EXISTS other_skills CASCADE;
DROP TABLE IF EXISTS educations CASCADE;
DROP TABLE IF EXISTS profiles CASCADE;

-- Drop the old trigger function if it exists
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Portfolio API Database Schema
-- PostgreSQL / Supabase Compatible
-- Dataverse Sync Ready with Standard Audit Fields

-- Enable UUID extension (required for Supabase/PostgreSQL)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- Table: profiles
-- Description: Main portfolio profile information
-- =====================================================
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    bio TEXT,
    email VARCHAR(255),
    phone VARCHAR(50),
    location VARCHAR(255),
    skype VARCHAR(255),
    linkedin_url VARCHAR(255),
    github_url VARCHAR(255),
    profile_image_url VARCHAR(255),
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,  -- 0: Active, 1: Inactive
    status_code INT DEFAULT 1  -- 1: Active, 2: Inactive
);

-- =====================================================
-- Table: skill_categories
-- Description: Categories for technical skills
-- =====================================================
CREATE TABLE skill_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_order INTEGER DEFAULT 0,
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Table: skills
-- Description: Individual technical skills
-- =====================================================
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    category_id UUID REFERENCES skill_categories(id) ON DELETE CASCADE,
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Table: other_skills
-- Description: Non-categorized or soft skills
-- =====================================================
CREATE TABLE other_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Table: experiences
-- Description: Work experience entries
-- =====================================================
CREATE TABLE experiences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    period_display VARCHAR(100),
    tech_stack TEXT,
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Table: experience_duties
-- Description: Specific duties within work experiences
-- =====================================================
CREATE TABLE experience_duties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    description TEXT NOT NULL,
    experience_id UUID REFERENCES experiences(id) ON DELETE CASCADE,
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Table: experience_domains
-- Description: Business domains/industries for experiences
-- =====================================================
CREATE TABLE experience_domains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    experience_id UUID REFERENCES experiences(id) ON DELETE CASCADE,
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Table: educations
-- Description: Education history entries
-- =====================================================
CREATE TABLE educations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    school VARCHAR(255) NOT NULL,
    degree VARCHAR(200),
    major VARCHAR(200),
    education_year VARCHAR(50),
    
    -- Dataverse standard audit fields
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    state_code INT DEFAULT 0,
    status_code INT DEFAULT 1
);

-- =====================================================
-- Indexes for Performance Optimization
-- =====================================================
CREATE INDEX idx_skills_category_id ON skills(category_id);
CREATE INDEX idx_experience_duties_experience_id ON experience_duties(experience_id);
CREATE INDEX idx_experience_domains_experience_id ON experience_domains(experience_id);
CREATE INDEX idx_skill_categories_display_order ON skill_categories(display_order);

-- Indexes for state/status filtering (Dataverse compatibility)
CREATE INDEX idx_profiles_state_code ON profiles(state_code);
CREATE INDEX idx_skill_categories_state_code ON skill_categories(state_code);
CREATE INDEX idx_skills_state_code ON skills(state_code);
CREATE INDEX idx_other_skills_state_code ON other_skills(state_code);
CREATE INDEX idx_experiences_state_code ON experiences(state_code);
CREATE INDEX idx_experience_duties_state_code ON experience_duties(state_code);
CREATE INDEX idx_experience_domains_state_code ON experience_domains(state_code);
CREATE INDEX idx_educations_state_code ON educations(state_code);

-- =====================================================
-- Triggers for automatic modified_on timestamp
-- =====================================================
CREATE OR REPLACE FUNCTION update_modified_on_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_on = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_modified_on BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_skill_categories_modified_on BEFORE UPDATE ON skill_categories
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_skills_modified_on BEFORE UPDATE ON skills
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_other_skills_modified_on BEFORE UPDATE ON other_skills
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_experiences_modified_on BEFORE UPDATE ON experiences
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_experience_duties_modified_on BEFORE UPDATE ON experience_duties
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_experience_domains_modified_on BEFORE UPDATE ON experience_domains
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

CREATE TRIGGER update_educations_modified_on BEFORE UPDATE ON educations
    FOR EACH ROW EXECUTE FUNCTION update_modified_on_column();

-- =====================================================
-- Comments for Documentation
-- =====================================================
COMMENT ON TABLE profiles IS 'Main portfolio profile information - Dataverse sync ready';
COMMENT ON TABLE skill_categories IS 'Categories for organizing technical skills - Dataverse sync ready';
COMMENT ON TABLE skills IS 'Individual technical skills linked to categories - Dataverse sync ready';
COMMENT ON TABLE other_skills IS 'Soft skills and other non-categorized abilities - Dataverse sync ready';
COMMENT ON TABLE experiences IS 'Professional work experience entries - Dataverse sync ready';
COMMENT ON TABLE experience_duties IS 'Specific responsibilities within each work experience - Dataverse sync ready';
COMMENT ON TABLE experience_domains IS 'Business domains or industries for each experience - Dataverse sync ready';
COMMENT ON TABLE educations IS 'Educational background and qualifications - Dataverse sync ready';

-- =====================================================
-- Dataverse Field Mapping Reference
-- =====================================================
-- created_on    -> CreatedOn (Dataverse)
-- modified_on   -> ModifiedOn (Dataverse)
-- state_code    -> StateCode (0=Active, 1=Inactive)
-- status_code   -> StatusCode (1=Active, 2=Inactive)
-- id            -> [EntityName]Id (e.g., EducationId)
