const ProfileForm = ({ profile, onSave, onCancel }) => (
    <form className="space-y-4" onSubmit={(e) => {
        e.preventDefault();
        onSave({
            name: e.target.name.value,
            role: e.target.role.value,
            email: e.target.email.value,
            phone: e.target.phone.value,
            location: e.target.location.value,
            skype: e.target.skype.value,
            linkedin: e.target.linkedin.value,
            github: e.target.github.value,
        });
    }}>
        <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
                <label className="text-sm font-medium text-text-muted">Họ tên</label>
                <input name="name" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.name} />
            </div>
            <div className="space-y-2">
                <label className="text-sm font-medium text-text-muted">Email</label>
                <input name="email" type="email" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.email} />
            </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
                <label className="text-sm font-medium text-text-muted">Số điện thoại</label>
                <input name="phone" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.phone} />
            </div>
            <div className="space-y-2">
                <label className="text-sm font-medium text-text-muted">Skype</label>
                <input name="skype" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.skype} />
            </div>
        </div>
        <div className="space-y-2">
            <label className="text-sm font-medium text-text-muted">Vị trí</label>
            <input name="role" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.role} />
        </div>
        <div className="space-y-2">
            <label className="text-sm font-medium text-text-muted">Địa chỉ</label>
            <input name="location" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.location} />
        </div>
        <div className="space-y-2">
            <label className="text-sm font-medium text-text-muted">LinkedIn URL</label>
            <input name="linkedin" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.linkedin} />
        </div>
        <div className="space-y-2">
            <label className="text-sm font-medium text-text-muted">GitHub URL</label>
            <input name="github" className="w-full bg-white/5 border border-white/10 rounded-lg p-3 outline-none focus:border-primary/50 text-white" defaultValue={profile?.github} />
        </div>
        <div className="flex gap-4 pt-2">
            <button type="submit" className="flex-1 bg-primary hover:bg-primary-hover py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-primary/20">
                <Save size={18} /> Lưu
            </button>
            <button type="button" onClick={onCancel} className="px-8 py-3 bg-white/5 hover:bg-white/10 rounded-xl font-bold transition-all">Hủy</button>
        </div>
    </form>
);

export default ProfileForm;
