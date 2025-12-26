import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { User, Edit, LogIn, LogOut, Upload, Mail, MapPin, Briefcase, GraduationCap, Github, Linkedin, ExternalLink, Phone, Globe, Plus, X, Save, FileText, Eye, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import profileImg from './assets/profile.png';
import { usePortfolio } from './context/PortfolioContext';
import { useMutation } from './hooks/useApi';
import {
  profileService,
  experienceService,
  educationService,
  otherSkillService,
  skillCategoryService,
  skillService,
  cvService,
} from './services/portfolioService';
import { transformToApiFormat, transformFromApiFormat } from './utils/dataTransform';




// Mock Data - Fallback structure matching API format
const INITIAL_DATA = {
  profile: {
    name: "MINH NHAT, LE",
    role: "Senior Full Stack .NET, React | Lead / Senior Software Engineer",
    bio: "Chuyên gia phát triển hệ thống .NET Full Stack với hơn 14 năm kinh nghiệm. Có khả năng dẫn dắt đội ngũ lớn (hơn 11 người), thiết kế kiến trúc hệ thống từ Monolith đến Microservices, và triển khai trên các nền tảng Cloud hiện đại như AWS, Azure.",
    email: "nult2003@gmail.com",
    phone: "0982 880 258",
    location: "33/47 Street 4, Binh Hung Hoa Ward, Ho Chi Minh City, Viet Nam",
    skype: "nult2003@gmail.com",
    linkedin: "https://www.linkedin.com/in/minh-nhat-le-a9638919/",
  },
  skillsByCategory: {
    "Programming Languages": ["C#", "HTML", "CSS", "SASS", "JavaScript", "TypeScript", "SQL"],
    "Frameworks": ["MVC", "Entity Framework", "KnockoutJS", "VueJS", "React", ".NET Core Web API", "WCF", "WPF", "NUnit"],
    "Architect/Pattern": ["Repository pattern", "Microservices (RabbitMQ)", "Web Single Page", "MVC Architecture"],
    "ORM/Tools": ["Automapper", "Dapper", "Slapper", "Git", "Jira", "BitBucket", "Azure", "Visual Studio"],
    "Cloud/Infra": ["Docker", "Kubernetes (EKS)", "Terraform", "SAM", "EC2", "S3", "Minikube", "LENS"]
  },
  otherSkills: [
    "Training interns",
    "Analyze requirements from tickets/customers",
    "Leadership (Lead team over 11 members)",
    "Problem solving & Analytical thinking",
    "Excellent framework building skills (BE/FE)"
  ],
  experience: [
    {
      id: 1,
      company: "TMA Company",
      role: "Senior/Lead .NET Full Stack",
      period: "2020 - Hiện tại",
      domain: ["Network design management", "Clinical management"],
      techStack: "C#, Oracle, .NET Core Web API, Automapper, Entity Framework, Repository pattern, React, Redux, AWS S3, TypeScript",
      duties: [
        "Làm việc với các dự án từ Canada và Ấn Độ theo quy trình Agile.",
        "Phát triển ứng dụng dựa trên React và .NET Core API.",
        "Review code, Unit Test và quản lý mã nguồn qua Bitbucket.",
        "Quản lý team hơn 11 người, phân chia công việc và theo dõi tiến độ.",
        "Thảo luận trực tiếp với khách hàng về yêu cầu nghiệp vụ."
      ]
    },
    {
      id: 2,
      company: "XSPERA Company",
      role: "Senior .NET Full Stack",
      period: "09/2018 - 2020",
      domain: ["Web portal (Sharepoint)", "Logistic management"],
      techStack: "C#, SQL Server, .NET Core Web API, Automapper, Dapper, Entity Framework, React, Redux, Vue, TypeScript, Rabbit MQ",
      duties: [
        "Phân tích yêu cầu từ bộ phận kinh doanh để xây dựng ứng dụng với công nghệ phù hợp.",
        "Phát triển ứng dụng trên nền tảng SharePoint (On-premise & Online) kết hợp React và .NET Core.",
        "Tổ chức các buổi họp brainstorm để tìm kiếm giải pháp kỹ thuật tối ưu."
      ]
    }
  ],
  education: [
    {
      id: 1,
      school: "Post and Telecommunication Institute of Technology",
      degree: "Engineer's Degree",
      major: "Software Engineer"
    }
  ]
};


// Components
const Modal = ({ isOpen, onClose, title, children }) => (
  <AnimatePresence>
    {isOpen && (
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 w-full h-full">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        />
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="relative w-full max-w-2xl glass p-8 shadow-2xl overflow-y-auto max-h-[90vh]"
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
              {title}
            </h2>
            <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-full transition-colors">
              <X size={24} />
            </button>
          </div>
          {children}
        </motion.div>
      </div>
    )}
  </AnimatePresence>
);

// --- Form Components ---

const BioForm = ({ defaultValue, onSave, onCancel }) => (
  <form className="space-y-6" onSubmit={(e) => {
    e.preventDefault();
    onSave({ bio: e.target.bio.value });
  }}>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Nội dung giới thiệu</label>
      <textarea
        name="bio"
        className="w-full bg-white/5 border border-white/10 text-white focus:border-primary/50 outline-none transition-all min-h-[200px]"
        defaultValue={defaultValue}
      />
    </div>
    <div className="flex gap-4">
      <button type="submit" className="flex-1 btn-primary">
        <Save size={18} /> Lưu thay đổi
      </button>
      <button type="button" onClick={onCancel} className="btn-secondary px-8">Hủy</button>
    </div>
  </form>
);

const ExperienceForm = ({ item, onSave, onCancel }) => (
  <form className="space-y-4" onSubmit={(e) => {
    e.preventDefault();
    const duties = e.target.duties.value.split('\n').filter(d => d.trim() !== '');
    const domains = e.target.domains.value.split('\n').filter(d => d.trim() !== '');
    onSave({
      company: e.target.company.value,
      period: e.target.period.value,
      role: e.target.role.value,
      techStack: e.target.techStack.value,
      duties: duties,
      domain: domains
    });
  }}>
    <div className="grid grid-cols-2 gap-4">
      <div className="space-y-2">
        <label className="text-sm font-medium text-text-muted">Công ty</label>
        <input name="company" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.company} />
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium text-text-muted">Thời gian</label>
        <input name="period" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.period} />
      </div>
    </div>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Vị trí</label>
      <input name="role" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.role} />
    </div>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Công nghệ</label>
      <input name="techStack" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.techStack} />
    </div>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Dự án / Lĩnh vực (mỗi dòng một ý)</label>
      <textarea name="domains" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white min-h-[60px]" defaultValue={item?.domain?.join('\n')} />
    </div>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Nhiệm vụ (mỗi dòng một ý)</label>
      <textarea name="duties" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white min-h-[100px]" defaultValue={item?.duties?.join('\n')} />
    </div>
    <div className="flex gap-4 pt-2">
      <button type="submit" className="flex-1 btn-primary">
        <Save size={18} /> Lưu
      </button>
      <button type="button" onClick={onCancel} className="btn-secondary px-8">Hủy</button>
    </div>
  </form>
);

const EducationForm = ({ item, onSave, onCancel }) => (
  <form className="space-y-4" onSubmit={(e) => {
    e.preventDefault();
    onSave({
      school: e.target.school.value,
      degree: e.target.degree.value,
      major: e.target.major.value
    });
  }}>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Trường học</label>
      <input name="school" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.school} />
    </div>
    <div className="grid grid-cols-2 gap-4">
      <div className="space-y-2">
        <label className="text-sm font-medium text-text-muted">Bằng cấp</label>
        <input name="degree" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.degree} />
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium text-text-muted">Chuyên ngành</label>
        <input name="major" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={item?.major} />
      </div>
    </div>
    <div className="flex gap-4 pt-2">
      <button type="submit" className="flex-1 btn-primary">
        <Save size={18} /> Lưu
      </button>
      <button type="button" onClick={onCancel} className="btn-secondary px-8">Hủy</button>
    </div>
  </form>
);

const OtherSkillForm = ({ defaultValue, onSave, onCancel }) => (
  <form className="space-y-4" onSubmit={(e) => {
    e.preventDefault();
    onSave({ skill: e.target.skill.value });
  }}>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Kỹ năng</label>
      <input name="skill" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={defaultValue} />
    </div>
    <div className="flex gap-4 pt-2">
      <button type="submit" className="flex-1 btn-primary">
        <Save size={18} /> Lưu
      </button>
      <button type="button" onClick={onCancel} className="btn-secondary px-8">Hủy</button>
    </div>
  </form>
);

const SkillsForm = ({ category, skills, onSave, onCancel }) => (
  <form className="space-y-4" onSubmit={(e) => {
    e.preventDefault();
    const skillsList = e.target.skills.value.split(',').map(s => s.trim()).filter(s => s !== '');
    onSave({
      category: e.target.category.value,
      skills: skillsList
    });
  }}>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Tên nhóm kỹ năng</label>
      <input name="category" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white" defaultValue={category} />
    </div>
    <div className="space-y-2">
      <label className="text-sm font-medium text-text-muted">Kỹ năng (cách nhau bởi dấu phẩy)</label>
      <textarea name="skills" className="w-full bg-white/5 border border-white/10 outline-none focus:border-primary/50 text-white min-h-[80px]" defaultValue={skills?.join(', ')} />
    </div>
    <div className="flex gap-4 pt-2">
      <button type="submit" className="flex-1 btn-primary">
        <Save size={18} /> Lưu
      </button>
      <button type="button" onClick={onCancel} className="btn-secondary px-8">Hủy</button>
    </div>
  </form>
);

const PDFUploadModal = ({ isOpen, onClose, onAction, isProcessing }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
    } else {
      alert('Vui lòng chọn file PDF hợp lệ!');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Cập nhật thông tin từ CV (PDF)">
      <div className="space-y-6">
        {isProcessing ? (
          <div className="p-12 text-center space-y-4">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto"></div>
            <p className="text-white font-bold text-lg animate-pulse">Đang dùng AI phân tích CV của bạn...</p>
            <p className="text-text-muted text-sm italic">Quá trình này có thể mất vài giây tùy vào độ dài CV.</p>
          </div>
        ) : (
          <>
            <div className="p-8 border-2 border-dashed border-white/10 bg-white/5 text-center group hover:border-primary/40 transition-all">
              {!file ? (
                <label className="cursor-pointer block space-y-4">
                  <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                    <Upload className="text-primary" size={32} />
                  </div>
                  <div>
                    <p className="text-white font-bold text-lg">Chọn file PDF của bạn</p>
                    <p className="text-text-muted text-sm mt-1">Kéo thả hoặc nhấn để duyệt file</p>
                  </div>
                  <input type="file" accept=".pdf" className="hidden" onChange={handleFileChange} />
                </label>
              ) : (
                <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="space-y-4">
                  <div className="flex items-center gap-4 bg-primary/10 p-4 border border-primary/20">
                    <FileText className="text-primary" size={32} />
                    <div className="text-left">
                      <p className="text-white font-bold truncate max-w-[200px]">{file.name}</p>
                      <p className="text-primary text-xs uppercase tracking-widest font-bold">File đã sẵn sàng</p>
                    </div>
                    <button onClick={() => setFile(null)} className="ml-auto p-2 hover:bg-white/10 transition-colors whitespace-nowrap">
                      <RefreshCw size={18} /> Đổi file
                    </button>
                  </div>
                </motion.div>
              )}
            </div>

            {file && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-2 gap-4 pt-4">
                <button
                  onClick={() => onAction('preview', file)}
                  className="group flex flex-col items-center gap-3 p-6 glass hover:bg-primary/20 transition-all border border-white/10 hover:border-primary/30"
                >
                  <div className="p-3 bg-primary/10 group-hover:bg-primary/20 transition-colors">
                    <Eye className="text-primary" size={24} />
                  </div>
                  <div className="text-center">
                    <p className="font-bold text-white uppercase text-xs tracking-widest mb-1">Mode: Preview</p>
                    <p className="font-bold text-white text-lg">Xem trước</p>
                    <p className="text-xs text-text-muted mt-1 leading-relaxed">Phân tích dữ liệu & hiển thị,<br />không lưu vào Database.</p>
                  </div>
                </button>
                <button
                  onClick={() => onAction('replace', file)}
                  className="group flex flex-col items-center gap-3 p-6 glass hover:bg-accent/20 transition-all border border-white/10 hover:border-accent/30"
                >
                  <div className="p-3 bg-accent/10 group-hover:bg-accent/20 transition-colors">
                    <RefreshCw className="text-accent" size={24} />
                  </div>
                  <div className="text-center">
                    <p className="font-bold text-white uppercase text-xs tracking-widest mb-1">Mode: Replace</p>
                    <p className="font-bold text-white text-lg">Ghi đè</p>
                    <p className="text-xs text-text-muted mt-1 leading-relaxed">Phân tích & tự động cập nhật<br />trực tiếp vào Database.</p>
                  </div>
                </button>
              </motion.div>
            )}
          </>
        )}
      </div>
    </Modal>
  );
};

// --- End Form Components ---

const Navbar = ({ isAdmin, onToggleAdmin, onPDFAction, isProcessing }) => {
  const [isPDFModalOpen, setIsPDFModalOpen] = useState(false);

  return (
    <>
      <nav className="glass sticky top-4 z-50 mx-4 my-4 p-4 flex justify-between items-center px-8">
        <div className="flex items-center gap-8">
          <Link to="/" className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-emerald-400 bg-clip-text text-transparent">AI Portfolio</Link>
          {isAdmin && (
            <button
              onClick={() => setIsPDFModalOpen(true)}
              className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 hover:bg-white/10 transition-all text-sm font-medium"
            >
              <Upload size={16} className="text-primary" /> Cập nhật CV (PDF)
            </button>
          )}
        </div>
        <div className="flex gap-6 items-center">
          <Link to="/" className="hover:text-primary">Trang chủ</Link>
          <button
            onClick={onToggleAdmin}
            className={`flex items-center gap-2 px-6 py-2 rounded-full transition-all font-bold ${isAdmin ? 'btn-danger' : 'bg-primary/20 text-primary border border-primary/50 hover:bg-primary/30'}`}
          >
            {isAdmin ? <LogOut size={18} /> : <LogIn size={18} />}
            {isAdmin ? 'Thoát Admin' : 'Admin'}
          </button>
        </div>
      </nav>

      <PDFUploadModal
        isOpen={isPDFModalOpen}
        onClose={() => setIsPDFModalOpen(false)}
        isProcessing={isProcessing}
        onAction={(action, file) => {
          onPDFAction(action, file);
          // Don't close immediately if replace, let the handler manage it?
          // For now, we'll keep it as is, or maybe only close on success.
          if (action === 'replace') {
            // setIsPDFModalOpen(false); // will close when refetch happens?
          }
        }}
      />
    </>
  );
};

const Footer = () => (
  <footer className="mt-20 py-10 text-center border-t border-white/5 text-text-muted text-sm">
    <p>© 2025 AI Portfolio. All rights reserved.</p>
  </footer>
);


function App() {
  const [isAdmin, setIsAdmin] = useState(false);
  const { data: apiData, loading, error, refetch } = usePortfolio();
  const { mutate } = useMutation();
  const [editing, setEditing] = useState({ section: null, id: null });
  const [localData, setLocalData] = useState(null);
  const [isProcessingCV, setIsProcessingCV] = useState(false);
  const [extractedCVData, setExtractedCVData] = useState(null);

  // Use local data if available (for optimistic updates), otherwise API data or fallback
  const data = localData || apiData || INITIAL_DATA;

  // Update local data when API data changes
  React.useEffect(() => {
    if (apiData) {
      setLocalData(apiData);
    }
  }, [apiData]);

  const handleSave = async (section, formData) => {
    try {
      if (section === 'profile') {
        // Update entire profile
        if (data.profile?.id) {
          const profileData = transformToApiFormat.profile(formData);
          const updated = await mutate(profileService.updateProfile, data.profile.id, profileData);

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            profile: { ...prev.profile, ...formData }
          }));
        }
      } else if (section === 'bio') {
        // Update profile bio only
        if (data.profile?.id) {
          await mutate(profileService.updateProfile, data.profile.id, { bio: formData.bio });

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            profile: { ...prev.profile, bio: formData.bio }
          }));
        }
      } else if (section === 'exp') {
        if (editing.id === 'new') {
          const expData = transformToApiFormat.experience(formData);
          const newExp = await mutate(experienceService.create, expData);

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            experience: [transformFromApiFormat.experience(newExp), ...prev.experience]
          }));
        } else {
          const expData = transformToApiFormat.experience(formData);
          const updated = await mutate(experienceService.update, editing.id, expData);

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            experience: prev.experience.map(e =>
              e.id === editing.id ? transformFromApiFormat.experience(updated) : e
            )
          }));
        }
      } else if (section === 'edu') {
        if (editing.id === 'new') {
          const eduData = transformToApiFormat.education(formData);
          const newEdu = await mutate(educationService.create, eduData);

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            education: [transformFromApiFormat.education(newEdu), ...prev.education]
          }));
        } else {
          const eduData = transformToApiFormat.education(formData);
          const updated = await mutate(educationService.update, editing.id, eduData);

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            education: prev.education.map(e =>
              e.id === editing.id ? transformFromApiFormat.education(updated) : e
            )
          }));
        }
      } else if (section === 'otherSkills') {
        if (editing.id === 'new') {
          const newSkill = await mutate(otherSkillService.create, { name: formData.skill });

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            otherSkills: [...prev.otherSkills, { id: newSkill.id, name: formData.skill }]
          }));
        } else {
          // Update existing
          await mutate(otherSkillService.update, editing.id, { name: formData.skill });

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            otherSkills: prev.otherSkills.map(s =>
              s.id === editing.id ? { ...s, name: formData.skill } : s
            )
          }));
        }
      } else if (section === 'skills') {
        // Update existing skill category
        if (editing.id === 'new') {
          // This shouldn't happen, but handle it as create
          const newCategory = await mutate(skillCategoryService.create, {
            name: formData.category,
            display_order: Object.keys(data.skillsByCategory).length
          });

          // Add skills to the new category
          for (const skillName of formData.skills) {
            await mutate(skillService.create, {
              name: skillName,
              category_id: newCategory.id
            });
          }

          // Optimistic UI update
          setLocalData(prev => ({
            ...prev,
            skillsByCategory: {
              ...prev.skillsByCategory,
              [formData.category]: formData.skills
            }
          }));
        } else {
          // Update existing category - editing.id is the category name
          // Find the category ID from the backend
          let categoryId = null;
          try {
            const categories = await mutate(skillCategoryService.getAll);
            const cat = categories.find(c => c.name === editing.id);
            if (cat) {
              categoryId = cat.id;
            }
          } catch (e) {
            console.error('Failed to fetch categories', e);
          }

          // Determine which skills are new and need to be created
          const existingSkills = data.skillsByCategory[editing.id] || [];
          const newSkills = formData.skills.filter(s => !existingSkills.includes(s));
          if (categoryId) {
            for (const skillName of newSkills) {
              try {
                await mutate(skillService.create, { name: skillName, category_id: categoryId });
              } catch (e) {
                console.error('Failed to create skill', skillName, e);
              }
            }
          }

          // Optimistic UI update
          setLocalData(prev => {
            const newSkillsByCategory = { ...prev.skillsByCategory };
            const categoryName = editing.id; // old name
            if (categoryName !== formData.category) {
              delete newSkillsByCategory[categoryName];
            }
            newSkillsByCategory[formData.category] = formData.skills;
            return { ...prev, skillsByCategory: newSkillsByCategory };
          });

          // Note: Full backend sync would also handle renaming category and deleting removed skills.
        }
      } else if (section === 'skills-add') {
        // Create new skill category
        const newCategory = await mutate(skillCategoryService.create, {
          name: formData.category,
          display_order: Object.keys(data.skillsByCategory).length
        });

        // Add skills to the new category
        for (const skillName of formData.skills) {
          await mutate(skillService.create, {
            name: skillName,
            category_id: newCategory.id
          });
        }

        // Optimistic UI update
        setLocalData(prev => ({
          ...prev,
          skillsByCategory: {
            ...prev.skillsByCategory,
            [formData.category]: formData.skills
          }
        }));
      }

      setEditing({ section: null, id: null });
    } catch (err) {
      alert(`Error saving: ${err.message}`);
      // Revert to API data on error
      setLocalData(apiData);
    }
  };

  const handlePDFAction = async (action, fileData) => {
    setIsProcessingCV(true);
    try {
      // action can be 'preview' or 'replace'
      const response = await mutate(cvService.process, fileData, action);
      const analyzedData = response.data;
      setExtractedCVData(analyzedData);

      if (action === 'preview') {
        const transformed = transformFromApiFormat.cvExtraction(analyzedData);
        setLocalData(transformed);
        alert('Đã phân tích CV thành công! Bạn đang ở chế độ xem trước dữ liệu vừa trích xuất.');
      } else {
        // action === 'replace'
        alert('Hệ thống đã được cập nhật thành công từ CV của bạn!');
        refetch(); // Reload everything from backend
      }
    } catch (err) {
      alert(`Lỗi khi xử lý CV: ${err.message}`);
    } finally {
      setIsProcessingCV(false);
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-text-muted">Loading portfolio data...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center glass p-8 max-w-md">
          <p className="text-red-400 mb-4">Error loading data: {error}</p>
          <button
            onClick={refetch}
            className="bg-primary hover:bg-primary-hover px-6 py-2 rounded-lg font-bold"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }


  return (
    <Router>
      <div className="min-h-screen">
        <Navbar
          isAdmin={isAdmin}
          onToggleAdmin={() => setIsAdmin(!isAdmin)}
          onPDFAction={handlePDFAction}
          isProcessing={isProcessingCV}
        />

        <Routes>
          <Route path="/" element={
            <div className="container py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Sidebar Section */}
              <div className="lg:col-span-1 space-y-6">
                <motion.div initial={{ opacity: 0, x: -50 }} animate={{ opacity: 1, x: 0 }} className="glass p-8 text-center">
                  <div className="relative inline-block mb-6">
                    <img src={profileImg} alt="Profile" className="w-40 h-40 rounded-full object-cover border-4 border-primary/20" />
                    {isAdmin && <button className="absolute bottom-2 right-2 p-2 bg-primary rounded-full text-white shadow-lg"><Edit size={16} /></button>}
                  </div>
                  <div className="flex justify-between items-center mb-4">
                    <div className="flex-1" />
                    {isAdmin && editing.section !== 'profile' && (
                      <button
                        onClick={() => setEditing({ section: 'profile', id: data.profile?.id })}
                        className="btn-icon"
                      >
                        <Edit size={16} />
                      </button>
                    )}
                  </div>

                  {editing.section === 'profile' ? (
                    <div className="text-left">
                      <form className="space-y-4" onSubmit={(e) => {
                        e.preventDefault();
                        handleSave('profile', {
                          name: e.target.name.value,
                          role: e.target.role.value,
                          email: e.target.email.value,
                          phone: e.target.phone.value,
                          location: e.target.location.value,
                          skype: e.target.skype.value,
                          linkedin: e.target.linkedin.value,
                        });
                      }}>
                        <input name="name" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.name} placeholder="Họ tên" />
                        <input name="role" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.role} placeholder="Vị trí" />
                        <input name="email" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.email} placeholder="Email" />
                        <input name="phone" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.phone} placeholder="Số điện thoại" />
                        <input name="skype" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.skype} placeholder="Skype" />
                        <input name="location" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.location} placeholder="Địa chỉ" />
                        <input name="linkedin" className="w-full bg-white/5 border border-white/10 text-white" defaultValue={data.profile?.linkedin} placeholder="LinkedIn URL" />
                        <div className="flex gap-2 pt-2">
                          <button type="submit" className="flex-1 btn-primary py-2 text-sm">Lưu</button>
                          <button type="button" onClick={() => setEditing({ section: null, id: null })} className="px-4 btn-secondary py-2 text-sm">Hủy</button>
                        </div>
                      </form>
                    </div>
                  ) : (
                    <>
                      <h1 className="text-2xl font-bold mb-2">{data.profile?.name}</h1>
                      <p className="text-primary font-medium mb-6 uppercase tracking-wider text-xs">{data.profile?.role}</p>
                      <div className="space-y-4 text-left text-text-muted">
                        <div className="flex items-center gap-3"><Mail size={18} className="text-primary" /><span className="text-sm">{data.profile?.email}</span></div>
                        <div className="flex items-center gap-3"><Phone size={18} className="text-primary" /><span className="text-sm">{data.profile?.phone}</span></div>
                        <div className="flex items-center gap-3"><Globe size={18} className="text-primary" /><span className="text-sm">Skype: {data.profile?.skype}</span></div>
                        <div className="flex items-center gap-3"><MapPin size={18} className="text-primary" /><span className="text-sm">{data.profile?.location}</span></div>
                      </div>
                      <div className="mt-8 flex justify-center gap-4">
                        <a href="#" className="p-2 glass hover:bg-white/10 transition-colors"><Github size={20} /></a>
                        <a href={data.profile?.linkedin} target="_blank" rel="noopener noreferrer" className="p-2 glass hover:bg-white/10 transition-colors text-primary"><Linkedin size={20} /></a>
                      </div>
                    </>
                  )}
                </motion.div>

                {/* Tech Skills */}
                <motion.div initial={{ opacity: 0, x: -50 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="glass p-8">
                  <div className="flex justify-between items-center mb-6 border-b border-white/5 pb-2">
                    <h3 className="text-xl font-bold flex items-center gap-2"><Briefcase size={20} className="text-accent" /> Kỹ năng chuyên môn</h3>
                    {isAdmin && <button onClick={() => setEditing({ section: 'skills-add', id: 'new' })} className="btn-icon"><Plus size={18} /></button>}
                  </div>
                  <div className="space-y-6">
                    {editing.section === 'skills-add' && <SkillsForm onSave={(fd) => handleSave('skills', fd)} onCancel={() => setEditing({ section: null, id: null })} />}
                    {Object.entries(data.skillsByCategory).map(([category, skills]) => (
                      <div key={category} className="group relative">
                        {editing.section === 'skills' && editing.id === category ? (
                          <SkillsForm category={category} skills={skills} onSave={(fd) => handleSave('skills', fd)} onCancel={() => setEditing({ section: null, id: null })} />
                        ) : (
                          <>
                            <div className="flex justify-between items-center mb-2">
                              <p className="text-xs font-bold text-accent uppercase tracking-widest">{category}</p>
                              {isAdmin && <button onClick={() => setEditing({ section: 'skills', id: category })} className="opacity-0 group-hover:opacity-100 btn-icon w-6 h-6"><Edit size={10} /></button>}
                            </div>
                            <div className="flex flex-wrap gap-2">
                              {skills.map(skill => (
                                <span key={skill} className="px-3 py-1 bg-white/5 border border-white/10 rounded-md text-[11px] shadow-sm hover:border-primary/30 transition-colors">{skill}</span>
                              ))}
                            </div>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </motion.div>

                {/* Other Skills */}
                <motion.div initial={{ opacity: 0, x: -50 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="glass p-8">
                  <div className="flex justify-between items-center mb-6 border-b border-white/5 pb-2">
                    <h3 className="text-xl font-bold flex items-center gap-2"><User size={20} className="text-primary" /> Kỹ năng khác</h3>
                    {isAdmin && <button onClick={() => setEditing({ section: 'otherSkills-add', id: 'new' })} className="btn-icon"><Plus size={18} /></button>}
                  </div>
                  <div className="mb-4">
                    {editing.section === 'otherSkills-add' && (
                      <div className="mb-6 p-4 bg-white/5 rounded-xl border border-primary/20">
                        <OtherSkillForm onSave={(fd) => handleSave('otherSkills', fd)} onCancel={() => setEditing({ section: null, id: null })} />
                      </div>
                    )}
                  </div>
                  <ul className="space-y-3 text-sm text-text-muted">
                    {data.otherSkills.map((skill) => (
                      <li key={skill.id} className="group">
                        {editing.section === 'otherSkills' && editing.id === skill.id ? (
                          <div className="p-4 bg-white/5 rounded-xl border border-primary/20">
                            <OtherSkillForm defaultValue={skill.name} onSave={(fd) => handleSave('otherSkills', fd)} onCancel={() => setEditing({ section: null, id: null })} />
                          </div>
                        ) : (
                          <div className="flex items-start justify-between">
                            <div className="flex items-start gap-2"><span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 flex-shrink-0" />{skill.name}</div>
                            {isAdmin && <button onClick={() => setEditing({ section: 'otherSkills', id: skill.id })} className="opacity-0 group-hover:opacity-100 btn-icon w-6 h-6"><Edit size={10} /></button>}
                          </div>
                        )}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              </div>

              {/* Main Content Section */}
              <div className="lg:col-span-2 space-y-8">
                <motion.div initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} className="glass p-10">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold">Giới thiệu</h2>
                    {isAdmin && editing.section !== 'bio' && <button onClick={() => setEditing({ section: 'bio', id: 'main' })} className="btn-ghost-primary"><Edit size={16} /> Chỉnh sửa</button>}
                  </div>
                  {editing.section === 'bio' ? (
                    <BioForm defaultValue={data.profile?.bio} onSave={(fd) => handleSave('bio', fd)} onCancel={() => setEditing({ section: null, id: null })} />
                  ) : (
                    <p className="text-text-muted leading-relaxed text-lg">{data.profile?.bio}</p>
                  )}
                </motion.div>

                {/* Experience */}
                <motion.div initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass p-10">
                  <div className="flex justify-between items-center mb-8">
                    <h2 className="text-2xl font-bold">Kinh nghiệm làm việc</h2>
                    {isAdmin && <button onClick={() => setEditing({ section: 'exp-add', id: 'new' })} className="btn-ghost-primary"><Plus size={18} /> Thêm mới</button>}
                  </div>
                  <div className="flex flex-col">
                    {editing.section === 'exp-add' && <div className="mb-12 p-6 bg-white/5 rounded-2xl border border-primary/20"><ExperienceForm onSave={(fd) => handleSave('exp', fd)} onCancel={() => setEditing({ section: null, id: null })} /></div>}
                    {data.experience.map(exp => (
                      <div key={exp.id} className="relative pb-12 mb-12 border-b border-white/5 last:border-0 last:mb-0 last:pb-0 group">
                        {editing.section === 'exp' && editing.id === exp.id ? (
                          <ExperienceForm item={exp} onSave={(fd) => handleSave('exp', fd)} onCancel={() => setEditing({ section: null, id: null })} />
                        ) : (
                          <>
                            <div className="flex flex-col md:flex-row md:justify-between mb-6 gap-4 items-start">
                              <div>
                                <div className="flex items-center gap-3">
                                  <h4 className="text-xl font-bold text-white tracking-wide">{exp.role}</h4>
                                  {isAdmin && <button onClick={() => setEditing({ section: 'exp', id: exp.id })} className="opacity-0 group-hover:opacity-100 btn-icon w-7 h-7"><Edit size={14} /></button>}
                                </div>
                                <p className="text-primary font-bold text-lg">{exp.company}</p>
                              </div>
                              <span className="text-text-muted text-sm bg-white/5 border border-white/10 px-4 py-1 rounded-full shadow-inner">{exp.period}</span>
                            </div>
                            <div className="ml-6 space-y-6">
                              {exp.domain && (
                                <div>
                                  <p className="text-xs font-bold text-accent uppercase mb-3 tracking-widest flex items-center gap-2"><span className="w-1 h-1 bg-accent rounded-full"></span> Dự án / Lĩnh vực</p>
                                  <ul className="list-disc list-inside text-sm text-text-muted space-y-2 ml-4 leading-relaxed">{exp.domain.map((d, i) => <li key={i}>{d}</li>)}</ul>
                                </div>
                              )}
                              <div>
                                <p className="text-xs font-bold text-accent uppercase mb-3 tracking-widest flex items-center gap-2"><span className="w-1 h-1 bg-accent rounded-full"></span> Công nghệ</p>
                                <p className="text-sm text-white/80 italic ml-4 leading-relaxed bg-white/5 p-3 rounded-lg border border-white/5">{exp.techStack}</p>
                              </div>
                              <div>
                                <p className="text-xs font-bold text-accent uppercase mb-3 tracking-widest flex items-center gap-2"><span className="w-1 h-1 bg-accent rounded-full"></span> Nhiệm vụ chính</p>
                                <ul className="space-y-3 ml-4">{exp.duties.map((duty, i) => (<li key={i} className="text-sm text-text-muted flex gap-3 leading-relaxed"><span className="text-primary mt-1.5 flex-shrink-0 w-1.5 h-1.5 rounded-full border border-primary/50"></span>{duty}</li>))}</ul>
                              </div>
                            </div>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </motion.div>

                {/* Education */}
                <motion.div initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass p-10">
                  <div className="flex justify-between items-center mb-8">
                    <h2 className="text-2xl font-bold">Học vấn</h2>
                    {isAdmin && <button onClick={() => setEditing({ section: 'edu-add', id: 'new' })} className="btn-ghost-primary"><Plus size={16} /> Thêm mới</button>}
                  </div>
                  <div className="space-y-6">
                    {editing.section === 'edu-add' && <div className="p-6 bg-white/5 rounded-xl border border-primary/20"><EducationForm onSave={(fd) => handleSave('edu', fd)} onCancel={() => setEditing({ section: null, id: null })} /></div>}
                    {data.education.map(edu => (
                      <div key={edu.id} className="group relative">
                        {editing.section === 'edu' && editing.id === edu.id ? (
                          <div className="p-6 bg-white/5 rounded-xl border border-primary/20"><EducationForm item={edu} onSave={(fd) => handleSave('edu', fd)} onCancel={() => setEditing({ section: null, id: null })} /></div>
                        ) : (
                          <div className="flex flex-col md:flex-row md:justify-between md:items-center p-2 hover:bg-white/5 transition-all gap-4">
                            <div>
                              <div className="flex items-center gap-3 mb-1">
                                <h4 className="text-lg font-bold text-white">{edu.degree} in {edu.major}</h4>
                                {isAdmin && <button onClick={() => setEditing({ section: 'edu', id: edu.id })} className="opacity-0 group-hover:opacity-100 btn-icon w-7 h-7"><Edit size={14} /></button>}
                              </div>
                              <p className="text-primary font-medium">{edu.school}</p>
                            </div>
                            {edu.year && <span className="text-text-muted text-sm italic bg-white/5 px-3 py-1 rounded-full">{edu.year}</span>}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </motion.div>
              </div>
            </div>
          } />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
