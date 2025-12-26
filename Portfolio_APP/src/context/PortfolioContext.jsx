import React, { createContext, useContext, useState, useEffect } from 'react';
import {
    profileService,
    skillCategoryService,
    otherSkillService,
    experienceService,
    educationService,
} from '../services/portfolioService';
import { transformFromApiFormat } from '../utils/dataTransform';

const PortfolioContext = createContext();

export const usePortfolio = () => {
    const context = useContext(PortfolioContext);
    if (!context) {
        throw new Error('usePortfolio must be used within PortfolioProvider');
    }
    return context;
};

export const PortfolioProvider = ({ children }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAllData = async () => {
        try {
            setLoading(true);
            setError(null);

            const [profile, categories, otherSkills, experiences, educations] = await Promise.all([
                profileService.getProfile().catch(() => null),
                skillCategoryService.getAll(),
                otherSkillService.getAll(),
                experienceService.getAll(),
                educationService.getAll(),
            ]);

            setData({
                profile: profile ? transformFromApiFormat.profile(profile) : null,
                skillsByCategory: transformFromApiFormat.skillsByCategory(categories),
                otherSkills: transformFromApiFormat.otherSkills(otherSkills),
                experience: experiences.map(transformFromApiFormat.experience),
                education: educations.map(transformFromApiFormat.education),
            });
        } catch (err) {
            setError(err.message);
            console.error('Failed to fetch portfolio data:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAllData();
    }, []);

    const value = {
        data,
        loading,
        error,
        refetch: fetchAllData,
    };

    return (
        <PortfolioContext.Provider value={value}>
            {children}
        </PortfolioContext.Provider>
    );
};
