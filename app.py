from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Admin, HeroSection, PrincipalCard, Facility, VisionContent, ValueCard, AboutPageConfig, AboutPageValue, AboutPageAchievement, Notice, Event, AcademicCalendar, ContactQuery, AdmissionSetting, SubjectItem, DocItem, AdmissionQuery, AdmissionPageConfig, ContactPageConfig, FAQItem, GalleryPageConfig, GalleryPhoto, GalleryVideo, GalleryCategory, AcademicsPageConfig, AcademicsCurriculumCard, AcademicTopper, BirthdayRecord
import os
import datetime
import uuid
import email_function
from email_function import html_email_writer, html_email_fetcher, contact_query_fetcher, email_sender, html_admission_email_fetcher
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-for-production-102938'

db.init_app(app)

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images', 'uploaded')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return f"uploaded/{filename}"
    return None

@app.context_processor
def inject_contact_config():
    try:
        contact_config = ContactPageConfig.query.first()
        if not contact_config:
            contact_config = ContactPageConfig()
            db.session.add(contact_config)
            db.session.commit()
    except Exception:
        contact_config = None
    return dict(contact_config=contact_config)

# Ensure database tables and seed data are initialized
with app.app_context():
    # Dropping old admission page config table if schema has changed
    try:
        table_info = db.session.execute(db.text("PRAGMA table_info(admission_page_config)")).fetchall()
        if table_info:
            cols = [r[1] for r in table_info]
            if 'step1_title' not in cols or 'contact_label' not in cols:
                db.session.execute(db.text("DROP TABLE admission_page_config"))
                db.session.commit()
    except Exception as e:
        print("Migration check error:", e)

    try:
        table_info_contact = db.session.execute(db.text("PRAGMA table_info(contact_page_config)")).fetchall()
        if table_info_contact:
            cols_contact = [r[1] for r in table_info_contact]
            if 'whatsapp' not in cols_contact:
                db.session.execute(db.text("DROP TABLE contact_page_config"))
                db.session.commit()
    except Exception as e:
        print("Contact Migration check error:", e)

    db.create_all()
    # Seed default admin if none exist
    if not Admin.query.filter_by(username='admin').first():
        default_admin = Admin(username='admin')
        default_admin.set_password('admin123')
        db.session.add(default_admin)
        db.session.commit()
        
    # Seed default hero content if none exists
    if not HeroSection.query.first():
        default_hero = HeroSection(
            heading="St Xavier's High School Fatehpur",
            subheading="A clear path for potential",
            button_text="Enroll your child",
            description="Welcome to our school, where quality education, discipline, and proactive learning shape confident individuals. We inspire students to think creatively, act responsibly, develop strong character, and achieve excellence in every aspect of life."
        )
        db.session.add(default_hero)
        db.session.commit()

    # Seed default principal cards if none exist
    if not PrincipalCard.query.first():
        card1 = PrincipalCard(
            card_id='card1',
            title='FROM THE DESK OF',
            subtitle='Principal',
            image_url='principal.jpg',
            message_heading='Message from Principal',
            message_p1='Welcome to St Xavier High School. We believe in providing quality education and building a strong character for our students.',
            message_p2='Our faculty works tirelessly to guide every student toward academic and personal success.',
            signature_name='Principal Name',
            signature_role='Principal'
        )
        card2 = PrincipalCard(
            card_id='card2',
            title='FROM THE DESK OF',
            subtitle='Director',
            image_url='principal.jpg',
            message_heading='Message from Director',
            message_p1='Education is the key to unlocking potential. At St Xavier, we aim to provide an environment of excellence.',
            message_p2='We welcome all parents and children to join us in this journey of learning and growth.',
            signature_name='Director Name',
            signature_role='Director'
        )
        db.session.add_all([card1, card2])
        db.session.commit()

    # Seed default facilities if none exist
    if not Facility.query.first():
        f1 = Facility(icon='🧪', title='Modern Laboratories', description='State of the art science labs.', link='#')
        f2 = Facility(icon='📚', title='Smart Library', description='Vast collection of books and digital resources.', link='#')
        f3 = Facility(icon='🚌', title='Transport Service', description='Safe transport for all students.', link='#')
        f4 = Facility(icon='⚽', title='Sports Facilities', description='Promoting physical health and teamwork.', link='#')
        db.session.add_all([f1, f2, f3, f4])
        db.session.commit()

    # Seed default vision content if none exists
    if not VisionContent.query.first():
        default_vision = VisionContent(
            label='OUR VISION',
            heading='Shaping Future Leaders Through Excellence in Education',
            p1='At our institution, we envision a learning environment where curiosity is encouraged, character is nurtured, and excellence becomes a way of life. We strive to empower every student with the knowledge, confidence, and values needed to thrive in a rapidly changing world.',
            p2='Our vision extends beyond academic achievement. We aim to develop responsible citizens, innovative thinkers, compassionate leaders, and lifelong learners who contribute positively to society.',
            p3='Through a blend of modern education, strong ethical foundations, and holistic development, we prepare students to face future challenges with resilience and determination.'
        )
        db.session.add(default_vision)
        db.session.commit()

    # Seed default value cards if none exist
    if not ValueCard.query.first():
        v1 = ValueCard(number='01', title='Integrity', description='We encourage honesty and character in all actions.', image_url='integrity.jpg')
        v2 = ValueCard(number='02', title='Excellence', description='Striving for high standards in academics and beyond.', image_url='excellence.jpg')
        v3 = ValueCard(number='03', title='Leadership', description='Empowering students to take initiative and guide others.', image_url='leadership.jpg')
        db.session.add_all([v1, v2, v3])
        db.session.commit()
        
    # Seed default about page config if none exists
    if not AboutPageConfig.query.first():
        default_about_config = AboutPageConfig(
            hero_eyebrow="Est. tradition of excellence",
            hero_heading="About Our School",
            hero_description="A place where character is built alongside knowledge, and every student is known, challenged, and cared for.",
            who_eyebrow="Who We Are",
            who_heading="A community built on purpose",
            who_p1="We are a dedicated educational institution committed to nurturing young minds through academic excellence, character development, and holistic learning. Our school provides a supportive environment where students are encouraged to explore their potential, develop critical thinking skills, and become responsible citizens of tomorrow.",
            who_p2="With a team of experienced educators, modern teaching methodologies, and a student-centered approach, we strive to create lifelong learners prepared for future challenges and opportunities.",
            who_image_url="placeholder.jpg",
            history_eyebrow="School History",
            history_heading="Decades in the making",
            history_p1="Founded in [Year], our school began with a vision to provide quality education that combines academic rigor with strong moral values. Over the years, we have grown from a modest institution into a respected center of learning, serving generations of students and contributing to the educational development of our community.",
            history_p2="Our journey has been marked by continuous improvement, innovation in teaching practices, and a steadfast commitment to educational excellence.",
            history_image_url="placeholder.jpg",
            vm_eyebrow="Vision & Mission",
            vm_heading="What guides us forward",
            vm_vision_title="Our Vision",
            vm_vision_desc="To be a leading educational institution that inspires excellence, innovation, and integrity, empowering students to become confident, compassionate, and successful global citizens.",
            vm_mission_title="Our Mission",
            vm_mission_bullets="To provide high-quality education in a nurturing environment.\nTo foster intellectual curiosity and creativity.\nTo promote ethical values and social responsibility.\nTo encourage holistic development through academics, sports, arts, and co-curricular activities.\nTo prepare students for lifelong learning and leadership.",
            mgmt_eyebrow="Management",
            mgmt_heading="Leadership behind the vision",
            mgmt_p1="Our management team is dedicated to ensuring the highest standards of education, infrastructure, and student welfare. Through strategic planning, continuous improvement, and strong community engagement, the management works tirelessly to create an environment where students and staff can thrive.",
            mgmt_p2="Their leadership and vision guide the school toward achieving excellence in all aspects of education.",
            mgmt_image_url="placeholder.jpg",
            principal_eyebrow="Principal's Message",
            principal_heading="Welcome to our school.",
            principal_p1="Education is not merely the acquisition of knowledge but the development of character, confidence, and values that shape an individual's future. At our institution, we believe every child possesses unique talents and potential waiting to be discovered.",
            principal_p2="Our dedicated faculty strives to provide a safe, inspiring, and stimulating environment where students can learn, grow, and excel. We encourage curiosity, innovation, and a lifelong passion for learning.",
            principal_p3="Together with parents and the community, we are committed to preparing our students for success in an ever-changing world.",
            principal_signature_name="[Principal's Name]",
            principal_signature_role="Principal",
            principal_image_url="placeholder.jpg",
            achievements_banner_url="placeholder.jpg"
        )
        db.session.add(default_about_config)
        db.session.commit()

    # Seed default about page values if none exist
    if not AboutPageValue.query.first():
        av1 = AboutPageValue(
            icon_svg='<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l2.4 6.6L21 11l-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4z"/></svg>',
            title="Excellence",
            description="We strive for the highest standards in academics, conduct, and personal growth."
        )
        av2 = AboutPageValue(
            icon_svg='<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/></svg>',
            title="Integrity",
            description="We promote honesty, responsibility, and ethical behavior."
        )
        av3 = AboutPageValue(
            icon_svg='<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M5 21v-2a7 7 0 0114 0v2"/></svg>',
            title="Respect",
            description="We value diversity, inclusion, and mutual understanding."
        )
        av4 = AboutPageValue(
            icon_svg='<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-3 11c.5.4.8 1 .8 1.6V17h4.4v-1.4c0-.6.3-1.2.8-1.6A6 6 0 0012 3z"/></svg>',
            title="Innovation",
            description="We encourage creativity, critical thinking, and problem-solving."
        )
        av5 = AboutPageValue(
            icon_svg='<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21s-7-4.35-9.5-8.5C.8 9 2 5.5 5.5 5 8 4.6 10 6 12 8c2-2 4-3.4 6.5-3 3.5.5 4.7 4 3 7.5C19 16.65 12 21 12 21z"/></svg>',
            title="Compassion",
            description="We foster empathy, kindness, and social responsibility."
        )
        db.session.add_all([av1, av2, av3, av4, av5])
        db.session.commit()

    # Seed default about page achievements if none exist
    if not AboutPageAchievement.query.first():
        aa1 = AboutPageAchievement(text="Consistently excellent academic results.")
        aa2 = AboutPageAchievement(text="Outstanding performance in sports and athletics.")
        aa3 = AboutPageAchievement(text="Recognition in cultural, literary, and artistic competitions.")
        aa4 = AboutPageAchievement(text="Successful participation in science exhibitions and innovation programs.")
        aa5 = AboutPageAchievement(text="Strong alumni network contributing to various professional fields.")
        aa6 = AboutPageAchievement(text="Awards and certifications for educational excellence and community service.")
        db.session.add_all([aa1, aa2, aa3, aa4, aa5, aa6])
        db.session.commit()

    # Seed default notice cards if none exist
    if not Notice.query.first():
        n1 = Notice(
            category="Academic",
            date="18 Jun 2026",
            title="Term 3 Examination Schedule — Classes VI to XII",
            target="Classes VI – XII",
            content=(
                "The Examination Department is pleased to share the finalised timetable for Term 3 examinations commencing 14 July 2026. All examinations will be held in the Main Examination Hall from 9:00 AM to 12:00 PM unless otherwise stated.\n\n"
                "Students are reminded to carry their Admit Card and School Identity Card on all examination days. No student will be permitted entry without valid identification.\n\n"
                "Practical examinations for Science subjects (Classes IX–XII) will be conducted separately from 13–18 July. Individual schedules have been dispatched to class teachers."
            ),
            issued_by="Examination Department"
        )
        n2 = Notice(
            category="Fee",
            date="15 Jun 2026",
            title="Tuition Fee Payment — July Quarter Reminder",
            target="All Classes",
            content=(
                "This is a reminder that the July quarter fee is due by 30 June 2026. Parents and guardians are requested to ensure timely payment to avoid a late fee surcharge.\n\n"
                "Payments may be made via the school's online portal, demand draft in favour of \"St. Xavier's High School, Fatehpur,\" or directly at the Accounts Office between 9:00 AM and 1:00 PM on working days.\n\n"
                "Families facing financial difficulty are encouraged to contact the Accounts Office confidentially for assistance under the school's fee concession policy."
            ),
            issued_by="Accounts Office"
        )
        n3 = Notice(
            category="Holiday",
            date="12 Jun 2026",
            title="School Closure — Founders' Day Celebration",
            target="All Students & Staff",
            content=(
                "The school will remain closed on 25 June 2026 in observance of Founders' Day. This marks the 62nd anniversary of St. Xavier's High School, Fatehpur's establishment.\n\n"
                "A special assembly and award ceremony will be held on the morning of 24 June for students of Classes X–XII. Attendance is compulsory for all invited students. Formal uniform is required."
            ),
            issued_by="Principal's Office"
        )
        n4 = Notice(
            category="Sports",
            date="10 Jun 2026",
            title="Inter-School Athletics Meet — Team Selection Trials",
            target="Classes VII – XII",
            content=(
                "Students wishing to represent St. Xavier's High School, Fatehpur at the District Inter-School Athletics Meet (August 2026) must register for selection trials by 22 June 2026.\n\n"
                "Trials will be conducted on the school sports ground on 28 & 29 June from 6:00 AM to 8:30 AM. Events include 100m, 200m, 400m, long jump, high jump, shot put, and relay.\n\n"
                "Interested students must carry a valid fitness certificate from the school medical officer. Registrations are open at the Physical Education Department office."
            ),
            issued_by="Physical Education Dept."
        )
        n5 = Notice(
            category="General",
            date="08 Jun 2026",
            title="Library Book Return — End of Term Deadline",
            target="All Students",
            content=(
                "All students are requested to return borrowed library books by 5 July 2026. Books not returned by the due date will attract a replacement charge as per the school's library policy.\n\n"
                "Students with outstanding returns will be unable to issue new books for Term 3 until all dues are cleared. The Library will remain open Monday to Saturday, 8:00 AM – 4:00 PM."
            ),
            issued_by="School Librarian"
        )
        db.session.add_all([n1, n2, n3, n4, n5])
        db.session.commit()

    # Seed default events if none exist
    if not Event.query.first():
        e1 = Event(
            title="Annual Science & Innovation Fair 2026",
            date="3 & 4 June 2026",
            description="Over 120 students from Classes VI to XII presented original science projects, working models, and research findings at this year's Science & Innovation Fair. The event drew participation from eleven visiting schools and was evaluated by a panel of academics and industry professionals. Projects ranged from sustainable energy solutions to AI-powered assistive technology. This year's Gold Award was claimed by a Class XI team for their bio-degradable water filtration prototype.",
            image1_url="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=900&q=80",
            image2_url="https://images.unsplash.com/photo-1532094349884-543559244000?w=500&q=80",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_thumb_url="https://images.unsplash.com/photo-1518152006812-edab29b069ac?w=500&q=80",
            tags="Academic, STEM, Competition, All Classes"
        )
        e2 = Event(
            title="St. Xavier's Cultural Evening 2026",
            date="24 May 2026",
            description="The school's most-anticipated evening of the academic year returned in full splendour with performances spanning classical dance, instrumental music, drama, and spoken word poetry. More than 200 students took to the stage before an audience of families, faculty, and distinguished guests. This year's theme — Voices of Tomorrow — celebrated the creative expression and cultural heritage of our student community. The evening concluded with a choral ensemble that received a standing ovation from the packed auditorium.",
            image1_url="https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=900&q=80",
            image2_url="https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=500&q=80",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_thumb_url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&q=80",
            tags="Cultural, Performing Arts, Community"
        )
        e3 = Event(
            title="Annual Inter-House Sports Day 2026",
            date="10 May 2026",
            description="The annual Inter-House Sports Day brought the school grounds to life with athletic spirit and friendly competition. Students from all four houses — Ashoka, Tagore, Raman, and Sarojini — competed across 18 track and field events. Ashoka House claimed the overall championship trophy for the second consecutive year, while Raman House swept the field events. The day concluded with a prize distribution ceremony presided over by the School Director and honoured guests from the Parent-Teacher Association.",
            image1_url="https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=900&q=80",
            image2_url="https://images.unsplash.com/photo-1551958219-acbc595d7a4d?w=500&q=80",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_thumb_url="https://images.unsplash.com/photo-1526676317768-d9b14f15615a?w=500&q=80",
            tags="Sports, Athletics, Inter-House, All Classes"
        )
        db.session.add_all([e1, e2, e3])
        db.session.commit()

    # Seed default academic calendar if none exists
    if not AcademicCalendar.query.first():
        default_calendar = AcademicCalendar(image_url="Annual_planner.png")
        db.session.add(default_calendar)
        db.session.commit()

    # Seed default admission settings if none exist
    if not AdmissionSetting.query.first():
        setting = AdmissionSetting(
            admissions_open=True,
            closed_message_heading="Admissions Closed",
            closed_message_body="Thank you for your interest. Admissions for the current academic session are now closed. Please check back later."
        )
        db.session.add(setting)
        db.session.commit()

    # Seed default subject items if none exist
    if not SubjectItem.query.first():
        s1 = SubjectItem(title="English Language & Comprehension", svg_icon="pencil")
        s2 = SubjectItem(title="Mathematics & Numeracy", svg_icon="chart")
        s3 = SubjectItem(title="General Awareness", svg_icon="globe")
        s4 = SubjectItem(title="Logical Reasoning & Aptitude", svg_icon="lightbulb")
        s5 = SubjectItem(title="Environmental Science (Class V and above)", svg_icon="book")
        db.session.add_all([s1, s2, s3, s4, s5])
        db.session.commit()

    # Seed default doc items if none exist
    if not DocItem.query.first():
        d1 = DocItem(name="Birth Certificate", note="Original + photocopy required", svg_icon="certificate")
        d2 = DocItem(name="Previous School Report Card", note="Most recent mark sheet / progress report", svg_icon="report_card")
        d3 = DocItem(name="Transfer Certificate (T.C.)", note="Mandatory for students from other schools", svg_icon="transfer_cert")
        d4 = DocItem(name="Passport Size Photographs", note="4 recent passport photographs", svg_icon="photograph")
        d5 = DocItem(name="Aadhaar Card Copy", note="Student's Aadhaar (if applicable)", svg_icon="id_card")
        db.session.add_all([d1, d2, d3, d4, d5])
        db.session.commit()

    # Seed default admission page config if none exists
    if not AdmissionPageConfig.query.first():
        default_config = AdmissionPageConfig(
            hero_eyebrow="Admissions 2025–26",
            hero_heading="Begin Your Journey at Greenfield Academy",
            hero_subheading="Join a learning environment that nurtures academic excellence, discipline, and character. Admissions are now open for the upcoming academic year.",
            overview_eyebrow="Admission Overview",
            overview_heading="How Admissions Work",
            overview_p1="Students seeking admission are required to complete the admission process and fulfil all eligibility requirements prescribed by the school.",
            overview_p2="Admission is granted strictly on the basis of the candidate's performance in the admission test and is not influenced by marks or grades obtained at any prior institution.",
            visit_title="Visit Us in Person",
            visit_text="Parents and guardians are welcome to visit the school office directly for admission, information, or any related queries during office hours.",
            office_days="Monday – Saturday",
            office_hours="09:00 AM – 02:00 PM",
            office_note="Office remains closed on Sundays and public holidays.",
            process_eyebrow="Admission Process",
            process_heading="Six Steps to Enrollment",
            process_text="Our admission process is designed to be straightforward and transparent. Here is what you can expect from the moment you apply to the day your child joins us.",
            test_heading="What to Expect",
            test_p1="All students applying for admission are required to appear for an admission test comprising a written examination conducted at the school premises.",
            test_p2="No specific syllabus is prescribed for the admission test. Candidates should possess a sound knowledge of subjects appropriate for the class lower than the one for which admission is sought.",
            test_p3="Admission is granted strictly on the basis of the candidate's performance in the admission test and not on marks obtained elsewhere.",
            test_note="Please Note: The admission test cannot be rescheduled except under exceptional circumstances at the sole discretion of the school administration.",
            
            # Seed Steps
            step1_title="Submit the Online Admission Form",
            step1_text="Complete and submit the admission form through our online portal or collect a physical copy from the school office. Ensure all details are accurate before submission.",
            step2_title="Admission Team Contact",
            step2_text="Once your application is received, a member of our admissions team will review the details and contact you to confirm the next steps and the date for the admission test.",
            step3_title="Appear for the Admission Test",
            step3_text="The candidate must appear in person for a written admission test conducted at the school premises on the designated date and time communicated by the admissions team.",
            step4_title="Admission Test Evaluation",
            step4_text="The written examination is evaluated by the school's academic panel. Results are assessed on the basis of the candidate's knowledge and aptitude for the class applied for.",
            step5_title="Submission of Required Documents",
            step5_text="Candidates who qualify the admission test are required to submit all mandatory documents to the school office within the timeframe specified by the admissions team.",
            step6_title="Confirmation of Admission",
            step6_text="Upon verification of documents and completion of the admission fee, the admission is formally confirmed and a welcome letter is issued to the student and family.",
            
            # Seed Documents
            doc_eyebrow="Required Documents",
            doc_heading="Documents to Submit",
            doc_text="The following documents must be submitted to the school office after the candidate has qualified the admission test and before admission can be confirmed.",
            tc_notice_heading="Transfer Certificate Notice:",
            tc_notice_text="Admission can be finalised only after submission of a valid Transfer Certificate (T.C.). Transfer Certificates issued by schools outside Uttar Pradesh must be countersigned by the education authorities of the respective state before submission.",
            
            # Seed Two Ways
            ways_eyebrow="How to Apply",
            ways_heading="Two Ways to Begin",
            ways_text="You may apply for admission through our online form or visit the school office directly — whichever is most convenient for your family. Our team will guide you through every step.",
            way1_title="Apply Online",
            way1_text="Fill out the admission form below. Once submitted, our admissions team will review your application and reach out to you with the next steps and required guidance.",
            way2_title="Visit the School Office",
            way2_text="Parents and guardians are welcome to visit the school office directly during office hours for admission inquiries, assistance, or to collect a physical form.",
            
            # Seed Form Intro
            form_eyebrow="Online Application",
            form_heading="Submit Your Application",
            form_text="Complete the form below to begin the admission process. Our team will contact you within 2 working days to confirm your application and provide further guidance.",

            # Seed Contact Strip Info
            contact_label="Get in Touch",
            contact_title="Admissions Office",
            contact_phone="+91 12345 67890",
            contact_email="admissions@greenfieldacademy.edu.in",
            contact_address="123 Academy Road, Lucknow, U.P.",
            contact_map_link="#"
        )
        db.session.add(default_config)
        db.session.commit()

    # Seed default contact page config if none exists
    if not ContactPageConfig.query.first():
        default_contact_config = ContactPageConfig(
            address_line1="G.T. Road, Reraiya, Near Dak Bunglow",
            address_line2="Fatehpur, Uttar Pradesh - 212601",
            phone1="+91 70801 23456",
            phone2="+91 5180 223456",
            email1="info@stxaviersfatehpur.org",
            email2="admissions@stxaviersfatehpur.org",
            whatsapp="+91 70801 23456",
            office_hours_mon_fri="8:00 AM – 4:00 PM",
            office_hours_sat="8:00 AM – 1:00 PM",
            office_hours_sun="Closed",
            school_hours_primary="8:00 AM – 1:30 PM",
            school_hours_middle="8:00 AM – 2:30 PM",
            school_hours_senior="8:00 AM – 3:00 PM",
            admission_hours_mon_sat="9:00 AM – 3:00 PM",
            admission_hours_sun="Closed",
            admission_hours_note="* Timings may vary during exams and holidays",
            map_iframe_src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3596.223871780447!2d80.81422797523956!3d25.666993177402636!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x399d8d002a2012d9%3A0x6d05f3241b714b2e!2sSt.%20Xavier&#39;s%20High%20School!5e0!3m2!1sen!2sin!4v1718870000000!5m2!1sen!2sin",
            map_directions_url="https://maps.google.com/?q=St.+Xavier's+High+School+Fatehpur+Uttar+Pradesh"
        )
        db.session.add(default_contact_config)
        db.session.commit()

    # Seed default FAQs if none exist
    if not FAQItem.query.first():
        f1 = FAQItem(
            question="How can I apply for admission?",
            answer="You can apply for admission by visiting the school administrative office to collect the registration form or by applying online through our Admissions portal during the active admission cycle (December to March)."
        )
        f2 = FAQItem(
            question="What documents are required for admission?",
            answer="Key documents include: 1) Birth Certificate, 2) Transfer Certificate (from the previous school), 3) Report card of the last qualified class, 4) Passport size photographs, and 5) Aadhaar Card of child & parents."
        )
        f3 = FAQItem(
            question="What is the fee structure?",
            answer="Our fee structure varies by grade level. Detailed term fees, tuition fees, and admission fee lists can be collected from the school accounts office or requested via email at info@stxaviersfatehpur.org."
        )
        f4 = FAQItem(
            question="Does the school provide transportation?",
            answer="Yes, St Xavier High School provides safe, GPS-enabled school bus transportation covering major routes across Fatehpur and surrounding areas. All buses have trained attendants and speed limiters."
        )
        f5 = FAQItem(
            question="How can I schedule a campus visit?",
            answer="Campus visits can be scheduled in advance by calling the reception desk or sending an email. Tours are typically guided by our admissions officer and conducted on working days between 9:00 AM and 1:00 PM."
        )
        f6 = FAQItem(
            question="What are the school's board affiliations?",
            answer="St Xavier High School, Fatehpur is affiliated with the Council for the Indian School Certificate Examinations (CISCE), New Delhi, offering ICSE (Grade X) and ISC (Grade XII) curriculums."
        )
        db.session.add_all([f1, f2, f3, f4, f5, f6])
        db.session.commit()

    # Seed default GalleryPageConfig if none exists
    if not GalleryPageConfig.query.first():
        default_gallery_config = GalleryPageConfig()
        db.session.add(default_gallery_config)
        db.session.commit()

    # Seed default GalleryCategory items if none exist
    if not GalleryCategory.query.first():
        categories = [
            GalleryCategory(name="Campus & Infrastructure", slug="campus"),
            GalleryCategory(name="Classrooms & Labs", slug="classroom"),
            GalleryCategory(name="Sports & Games", slug="sports"),
            GalleryCategory(name="Cultural Events & Activities", slug="cultural")
        ]
        db.session.add_all(categories)
        db.session.commit()

    # Seed default GalleryPhoto items if none exist
    if not GalleryPhoto.query.first():
        photos = [
            GalleryPhoto(category="campus", img_url="https://images.unsplash.com/photo-1562774053-701939374585?w=600&auto=format&fit=crop&q=75", caption="Main Academic Block"),
            GalleryPhoto(category="campus", img_url="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&auto=format&fit=crop&q=75", caption="Library & Knowledge Centre"),
            GalleryPhoto(category="campus", img_url="https://images.unsplash.com/photo-1580537659466-0a9bfa916a54?w=600&auto=format&fit=crop&q=75", caption="Campus Entrance Gate"),
            GalleryPhoto(category="campus", img_url="https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&auto=format&fit=crop&q=75", caption="Open Air Amphitheatre"),
            GalleryPhoto(category="classroom", img_url="https://images.unsplash.com/photo-1532094349884-543559a8e1c3?w=600&auto=format&fit=crop&q=75", caption="Modern Science Laboratory"),
            GalleryPhoto(category="classroom", img_url="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&auto=format&fit=crop&q=75", caption="Smart Classroom"),
            GalleryPhoto(category="classroom", img_url="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop&q=75", caption="Computer Science Lab"),
            GalleryPhoto(category="classroom", img_url="https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600&auto=format&fit=crop&q=75", caption="Art Studio"),
            GalleryPhoto(category="sports", img_url="https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=600&auto=format&fit=crop&q=75", caption="Annual Athletics Championship"),
            GalleryPhoto(category="sports", img_url="https://images.unsplash.com/photo-1546519638405-a9d1b14c3bd1?w=600&auto=format&fit=crop&q=75", caption="Basketball Interschool Finals"),
            GalleryPhoto(category="sports", img_url="https://images.unsplash.com/photo-1600965962361-9035dbfd1c50?w=600&auto=format&fit=crop&q=75", caption="Swimming Gala"),
            GalleryPhoto(category="sports", img_url="https://images.unsplash.com/photo-1593766788306-28561086694e?w=600&auto=format&fit=crop&q=75", caption="Cricket Training Session"),
            GalleryPhoto(category="cultural", img_url="https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=600&auto=format&fit=crop&q=75", caption="Annual Day Celebration 2024"),
            GalleryPhoto(category="cultural", img_url="https://images.unsplash.com/photo-1464802686167-b939a6910659?w=600&auto=format&fit=crop&q=75", caption="National Science Exhibition"),
            GalleryPhoto(category="cultural", img_url="https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600&auto=format&fit=crop&q=75", caption="Music & Dance Festival"),
            GalleryPhoto(category="cultural", img_url="https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=600&auto=format&fit=crop&q=75", caption="Graduation Ceremony 2024")
        ]
        db.session.add_all(photos)
        db.session.commit()

    # Seed default GalleryVideo items if none exist
    if not GalleryVideo.query.first():
        videos = [
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Annual Day 2024 — A Grand Celebration", duration="18:42", thumbnail_url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Inter-School Science Olympiad", duration="12:15", thumbnail_url="https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Sports Day 2024 — Highlights Reel", duration="9:30", thumbnail_url="https://images.unsplash.com/photo-1519861531473-9200262188bf?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Campus Tour — Walk Through Greenfield", duration="6:50", thumbnail_url="https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Graduation Ceremony — Class of 2024", duration="22:10", thumbnail_url="https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Robotics Club — Regional Championship", duration="8:05", thumbnail_url="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Cultural Fiesta — Music & Dance Night", duration="15:20", thumbnail_url="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Debate Championship — State Finals", duration="28:45", thumbnail_url="https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=640&auto=format&fit=crop&q=70"),
            GalleryVideo(yt_id="dQw4w9WgXcQ", title="Founder's Day — 12th Anniversary", duration="11:33", thumbnail_url="https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=640&auto=format&fit=crop&q=70")
        ]
        db.session.add_all(videos)
        db.session.commit()

    # Seed default AcademicsPageConfig if none exists
    if not AcademicsPageConfig.query.first():
        default_academics_config = AcademicsPageConfig()
        db.session.add(default_academics_config)
        db.session.commit()

    # Seed default AcademicsCurriculumCard items if none exist
    if not AcademicsCurriculumCard.query.first():
        cards = [
            AcademicsCurriculumCard(
                icon_svg='<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 14l9-5-9-5-9 5 9 5z"/><path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/></svg>',
                title="Primary School",
                classes_range="Classes I–V",
                description="Building strong foundations in language, mathematics, environmental awareness, and creative expression through activity-based learning."
            ),
            AcademicsCurriculumCard(
                icon_svg='<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>',
                title="Middle School",
                classes_range="Classes VI–VIII",
                description="Introducing broader subject areas and conceptual understanding. Emphasis on analytical thinking, project work, and communication."
            ),
            AcademicsCurriculumCard(
                icon_svg='<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
                title="Secondary",
                classes_range="Classes IX–X",
                description="Preparing students for academic excellence while fostering independent learning habits, continuous assessments, and practical applications."
            ),
            AcademicsCurriculumCard(
                icon_svg='<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
                title="Senior Secondary",
                classes_range="Classes XI–XII",
                description="Specialized academic streams (Science, Commerce, Math) preparing learners for higher education and competitive examinations."
            )
        ]
        db.session.add_all(cards)
        db.session.commit()

    # Seed default AcademicTopper items if none exist
    if not AcademicTopper.query.first():
        toppers = [
            AcademicTopper(
                title="Class X CBSE Board Outstanding Achievers",
                class_name="Class X",
                year="2024-2025",
                image_url="topper.jpg",
                description="Congratulations to our stellar Class X scholars on their exceptional performance in the CBSE Board Examinations! Your dedication and academic excellence continue to make the school proud."
            ),
            AcademicTopper(
                title="Class XI Academic Stars & Stream Toppers",
                class_name="Class XI",
                year="2024-2025",
                image_url="topper2.jpg",
                description="Honoring our brilliant Class XI academic toppers for their outstanding achievements across Science, Commerce, and Humanities. You pave the way for future board successes!"
            )
        ]
        db.session.add_all(toppers)
        db.session.commit()

    # Seed default BirthdayRecord items if none exist
    if not BirthdayRecord.query.first():
        birthdays = [
            BirthdayRecord(
                name="Sarah Jenkins",
                birthday="28th June",
                role="Teacher",
                class_name="English Dept.",
                image_url="class.jpg"
            ),
            BirthdayRecord(
                name="Aarav Sharma",
                birthday="29th June",
                role="Student",
                class_name="Class X-A",
                image_url="topper.jpg"
            ),
            BirthdayRecord(
                name="Mrs. Priya Patel",
                birthday="1st July",
                role="Teacher",
                class_name="Science Dept.",
                image_url="topper2.jpg"
            ),
            BirthdayRecord(
                name="Rohan Das",
                birthday="4th July",
                role="Student",
                class_name="Class IX-B",
                image_url="class1.jpg"
            ),
            BirthdayRecord(
                name="Neha Gupta",
                birthday="10th July",
                role="Student",
                class_name="Class XI-C",
                image_url="building1.jpg"
            )
        ]
        db.session.add_all(birthdays)
        db.session.commit()

# md loggers
def log_hero_change(username, old_hero, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (by {username})\n"
    log_entry += f"* **Changes applied via Admin Dashboard**:\n"
    
    has_changes = False
    
    if old_hero.heading != form_data['heading']:
        log_entry += f"  * **Heading**: \"{old_hero.heading}\" &rarr; \"{form_data['heading']}\"\n"
        has_changes = True
    if old_hero.subheading != form_data['subheading']:
        log_entry += f"  * **Tagline**: \"{old_hero.subheading}\" &rarr; \"{form_data['subheading']}\"\n"
        has_changes = True
    if old_hero.button_text != form_data['button_text']:
        log_entry += f"  * **Button Text**: \"{old_hero.button_text}\" &rarr; \"{form_data['button_text']}\"\n"
        has_changes = True
    if old_hero.description != form_data['description']:
        old_desc_escaped = old_hero.description.replace('\n', ' ')
        new_desc_escaped = form_data['description'].replace('\n', ' ')
        log_entry += f"  * **Description**: \"{old_desc_escaped}\" &rarr; \"{new_desc_escaped}\"\n"
        has_changes = True
        
    if not has_changes:
        log_entry += "  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_vision_change(username, old_vision, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Vision Updated by {username})\n"
    log_entry += f"* **Administrator updated Vision Section**:\n"
    
    has_changes = False
    if old_vision.label != form_data['label']:
        log_entry += f"  * **Label**: \"{old_vision.label}\" &rarr; \"{form_data['label']}\"\n"
        has_changes = True
    if old_vision.heading != form_data['heading']:
        log_entry += f"  * **Heading**: \"{old_vision.heading}\" &rarr; \"{form_data['heading']}\"\n"
        has_changes = True
    if old_vision.p1 != form_data['p1']:
        log_entry += f"  * **Paragraph 1**: \"{old_vision.p1}\" &rarr; \"{form_data['p1']}\"\n"
        has_changes = True
    if old_vision.p2 != form_data['p2']:
        log_entry += f"  * **Paragraph 2**: \"{old_vision.p2}\" &rarr; \"{form_data['p2']}\"\n"
        has_changes = True
    if old_vision.p3 != form_data['p3']:
        log_entry += f"  * **Paragraph 3**: \"{old_vision.p3}\" &rarr; \"{form_data['p3']}\"\n"
        has_changes = True
        
    if not has_changes:
        log_entry += "  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_principal_change(username, card_id, old_card, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Principal Card {card_id} Updated by {username})\n"
    log_entry += f"* **Administrator updated Principal Desk ({card_id})**:\n"
    
    has_changes = False
    for field in ['title', 'subtitle', 'image_url', 'message_heading', 'message_p1', 'message_p2', 'signature_name', 'signature_role']:
        if getattr(old_card, field) != form_data[field]:
            log_entry += f"  * **{field.replace('_', ' ').title()}**: \"{getattr(old_card, field)}\" &rarr; \"{form_data[field]}\"\n"
            has_changes = True
            
    if not has_changes:
        log_entry += "  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_facility_change(username, action, title, icon=None):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Facility {action} by {username})\n"
    if action == 'Added':
        log_entry += f"* **Administrator added a new facility card**:\n"
        log_entry += f"  * **Title**: \"{title}\"\n"
        if icon:
            log_entry += f"  * **Icon**: \"{icon}\"\n"
    elif action == 'Updated':
        log_entry += f"* **Administrator updated facility card \"{title}\"**:\n"
    elif action == 'Deleted':
        log_entry += f"* **Administrator deleted facility card \"{title}\"**:\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_value_change(username, action, title, number=None):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Value Card {action} by {username})\n"
    if action == 'Added':
        log_entry += f"* **Administrator added a new value card**:\n"
        log_entry += f"  * **Title**: \"{title}\"\n"
        if number:
            log_entry += f"  * **Number**: \"{number}\"\n"
    elif action == 'Updated':
        log_entry += f"* **Administrator updated value card \"{title}\"**:\n"
    elif action == 'Deleted':
        log_entry += f"* **Administrator deleted value card \"{title}\"**:\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_credential_change(username, old_username):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Credentials Updated by {username})\n"
    log_entry += f"* **Administrator updated security credentials**:\n"
    log_entry += f"  * **Username**: \"{old_username}\" &rarr; \"{username}\"\n"
    log_entry += f"  * **Password**: Updated successfully\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_about_content_change(username, section, old_data, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (About Page - {section} Updated by {username})\n"
    log_entry += f"* **Administrator updated About Page {section}**:\n"
    
    has_changes = False
    for field, old_val in old_data.items():
        new_val = form_data.get(field)
        if new_val is not None and old_val != new_val:
            old_escaped = str(old_val).replace('\n', ' ')
            new_escaped = str(new_val).replace('\n', ' ')
            log_entry += f"  * **{field.replace('_', ' ').title()}**: \"{old_escaped}\" &rarr; \"{new_escaped}\"\n"
            has_changes = True
            
    if not has_changes:
        log_entry += "  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_about_value_change(username, action, title):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (About Page Value {action} by {username})\n"
    if action == 'Added':
        log_entry += f"* **Administrator added a new About Page value card**:\n"
        log_entry += f"  * **Title**: \"{title}\"\n"
    elif action == 'Updated':
        log_entry += f"* **Administrator updated About Page value card \"{title}\"**:\n"
    elif action == 'Deleted':
        log_entry += f"* **Administrator deleted About Page value card \"{title}\"**:\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_about_achievement_change(username, action, text):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (About Page Achievement {action} by {username})\n"
    if action == 'Added':
        log_entry += f"* **Administrator added a new About Page achievement**:\n"
        log_entry += f"  * **Text**: \"{text}\"\n"
    elif action == 'Updated':
        log_entry += f"* **Administrator updated About Page achievement to \"{text}\"**:\n"
    elif action == 'Deleted':
        log_entry += f"* **Administrator deleted About Page achievement \"{text}\"**:\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_notice_change(username, action, title, category=None):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Notice Card {action} by {username})\n"
    if action == 'Added':
        log_entry += f"* **Administrator added a new notice card**:\n"
        log_entry += f"  * **Title**: \"{title}\"\n"
        if category:
            log_entry += f"  * **Category**: \"{category}\"\n"
    elif action == 'Updated':
        log_entry += f"* **Administrator updated notice card \"{title}\"**:\n"
    elif action == 'Deleted':
        log_entry += f"* **Administrator deleted notice card \"{title}\"**:\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_event_change(username, action, title):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Event {action} by {username})\n"
    if action == 'Added':
        log_entry += f"* **Administrator added a new event**: \"{title}\"\n"
    elif action == 'Updated':
        log_entry += f"* **Administrator updated event**: \"{title}\"\n"
    elif action == 'Deleted':
        log_entry += f"* **Administrator deleted event**: \"{title}\"\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")

def log_calendar_change(username, old_url, new_url):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Academic Calendar Updated by {username})\n"
    log_entry += f"* **Academic Calendar/Annual Planner image updated**:\n"
    log_entry += f"  * **Path/URL**: \"{old_url}\" &rarr; \"{new_url}\"\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_admission_setting_change(username, old_setting, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Admission Settings Updated by {username})\n"
    log_entry += f"* **Administrator updated Admission settings**:\n"
    
    if old_setting.admissions_open != form_data['admissions_open']:
        log_entry += f"  * **Admissions Open**: {old_setting.admissions_open} &rarr; {form_data['admissions_open']}\n"
    if old_setting.closed_message_heading != form_data['closed_message_heading']:
        log_entry += f"  * **Heading**: \"{old_setting.closed_message_heading}\" &rarr; \"{form_data['closed_message_heading']}\"\n"
    if old_setting.closed_message_body != form_data['closed_message_body']:
        log_entry += f"  * **Body**: \"{old_setting.closed_message_body}\" &rarr; \"{form_data['closed_message_body']}\"\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_subject_change(username, action, title):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Admission Subject {action} by {username})\n"
    log_entry += f"* **Administrator {action.lower()} admission subject \"{title}\"**:\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_document_change(username, action, name):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Admission Document {action} by {username})\n"
    log_entry += f"* **Administrator {action.lower()} required document \"{name}\"**:\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_admission_content_change(username, section, old_data, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Admission Content - {section} Updated by {username})\n"
    log_entry += f"* **Administrator updated Admission Page - {section} Section**:\n"
    
    has_changes = False
    for key, val in form_data.items():
        old_val = getattr(old_data, key, '')
        if old_val != val:
            log_entry += f"  * **{key.replace('_', ' ').title()}**: \"{old_val}\" &rarr; \"{val}\"\n"
            has_changes = True
            
    if not has_changes:
        log_entry += f"  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_contact_config_change(username, old_data, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Contact Page Config Updated by {username})\n"
    log_entry += f"* **Administrator updated Contact Page Config**:\n"
    
    has_changes = False
    for key, val in form_data.items():
        old_val = getattr(old_data, key, '')
        if old_val != val:
            log_entry += f"  * **{key.replace('_', ' ').title()}**: \"{old_val}\" &rarr; \"{val}\"\n"
            has_changes = True
            
    if not has_changes:
        log_entry += f"  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_faq_change(username, action, question):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (FAQ Item {action} by {username})\n"
    log_entry += f"* **Administrator {action.lower()} FAQ item: \"{question}\"**:\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_academics_config_change(username, old_data, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Academics Page Config Updated by {username})\n"
    log_entry += f"* **Administrator updated Academics Page Config**:\n"
    
    has_changes = False
    for key, val in form_data.items():
        old_val = getattr(old_data, key, '')
        if old_val != val:
            log_entry += f"  * **{key.replace('_', ' ').title()}**: \"{old_val}\" &rarr; \"{val}\"\n"
            has_changes = True
            
    if not has_changes:
        log_entry += f"  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_academics_curriculum_change(username, action, title):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Academics Curriculum {action} by {username})\n"
    log_entry += f"* **Administrator {action.lower()} curriculum card: \"{title}\"**:\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_academics_topper_change(username, action, name):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Academics Toppers {action} by {username})\n"
    log_entry += f"* **Administrator {action.lower()} topper: \"{name}\"**\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


@app.route("/")
def home():
    name = "Home"
    hero = HeroSection.query.first()
    principal_cards = PrincipalCard.query.all()
    facilities = Facility.query.all()
    vision = VisionContent.query.first()
    value_cards = ValueCard.query.all()
    notices = Notice.query.order_by(Notice.id.desc()).limit(2).all()
    latest_event = Event.query.order_by(Event.id.desc()).first()
    birthdays = BirthdayRecord.query.order_by(BirthdayRecord.id.asc()).all()
    return render_template(
        "index.html", 
        name=name, 
        hero=hero, 
        principal_cards=principal_cards, 
        facilities=facilities, 
        vision=vision, 
        value_cards=value_cards,
        notices=notices,
        latest_event=latest_event,
        birthdays=birthdays
    )


#routing

@app.route("/under-development")
def under_development():
    return render_template("under_development.html")

@app.route("/admin", methods=['GET','POST'])
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")
            
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = admin.username
            flash("Logged in successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password.", "error")
            
    return render_template("login.html")

@app.route("/admin/dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    hero = HeroSection.query.first()
    principal_cards = PrincipalCard.query.all()
    facilities = Facility.query.all()
    vision = VisionContent.query.first()
    value_cards = ValueCard.query.all()
    
    # Fetch About Page models
    about_config = AboutPageConfig.query.first()
    about_values = AboutPageValue.query.all()
    about_achievements = AboutPageAchievement.query.all()
    
    # Fetch Notice Cards
    notices = Notice.query.order_by(Notice.id.desc()).all()
    # Fetch Events
    events = Event.query.order_by(Event.id.desc()).all()
    # Fetch Academic Calendar
    calendar = AcademicCalendar.query.first()
    if not calendar:
        calendar = AcademicCalendar(image_url="Annual_planner.png")
        db.session.add(calendar)
        db.session.commit()

    # Fetch User Queries
    queries = ContactQuery.query.order_by(ContactQuery.id.desc()).all()
    
    # Fetch Admission-related models
    admission_setting = AdmissionSetting.query.first()
    if not admission_setting:
        admission_setting = AdmissionSetting(admissions_open=True)
        db.session.add(admission_setting)
        db.session.commit()
    admission_subjects = SubjectItem.query.all()
    admission_documents = DocItem.query.all()
    admission_queries = AdmissionQuery.query.order_by(AdmissionQuery.id.desc()).all()
    admission_config = AdmissionPageConfig.query.first()
    if not admission_config:
        admission_config = AdmissionPageConfig()
        db.session.add(admission_config)
        db.session.commit()
        
    # Fetch Contact Page Config & FAQs
    contact_config = ContactPageConfig.query.first()
    if not contact_config:
        contact_config = ContactPageConfig()
        db.session.add(contact_config)
        db.session.commit()
    faqs = FAQItem.query.order_by(FAQItem.id.asc()).all()

    # Fetch Gallery Page Config & Photos & Videos
    gallery_config = GalleryPageConfig.query.first()
    if not gallery_config:
        gallery_config = GalleryPageConfig()
        db.session.add(gallery_config)
        db.session.commit()
    gallery_photos = GalleryPhoto.query.all()
    gallery_videos = GalleryVideo.query.all()
    gallery_categories = GalleryCategory.query.order_by(GalleryCategory.id.asc()).all()
    
    # Fetch Academics Page Config & Curriculum Cards
    academics_config = AcademicsPageConfig.query.first()
    if not academics_config:
        academics_config = AcademicsPageConfig()
        db.session.add(academics_config)
        db.session.commit()
    academics_curriculum_cards = AcademicsCurriculumCard.query.order_by(AcademicsCurriculumCard.id.asc()).all()
    toppers = AcademicTopper.query.order_by(AcademicTopper.id.asc()).all()
    birthdays = BirthdayRecord.query.order_by(BirthdayRecord.id.asc()).all()
    
    active_tab = request.args.get('tab', 'hero')
    
    # Read activity logs from project_knowledge.md
    logs = ""
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                logs = f.read()
        except Exception as e:
            logs = f"Error reading activity logs: {e}"
            
    if request.method == 'POST':
        heading = request.form.get('heading', '').strip()
        subheading = request.form.get('subheading', '').strip()
        button_text = request.form.get('button_text', '').strip()
        description = request.form.get('description', '').strip()
        
        if not heading or not subheading or not button_text or not description:
            flash("All hero section fields are required.", "error")
            return render_template(
                "dashboard.html", 
                hero=hero, 
                principal_cards=principal_cards, 
                facilities=facilities, 
                vision=vision, 
                value_cards=value_cards,
                about_config=about_config,
                about_values=about_values,
                about_achievements=about_achievements,
                notices=notices,
                events=events,
                calendar=calendar,
                queries=queries,
                admission_setting=admission_setting,
                admission_subjects=admission_subjects,
                admission_documents=admission_documents,
                admission_queries=admission_queries,
                admission_config=admission_config,
                contact_config=contact_config,
                faqs=faqs,
                gallery_config=gallery_config,
                gallery_photos=gallery_photos,
                gallery_videos=gallery_videos,
                gallery_categories=gallery_categories,
                academics_config=academics_config,
                academics_curriculum_cards=academics_curriculum_cards,
                toppers=toppers,
                birthdays=birthdays,
                active_tab='hero', 
                logs=logs
            )
            
        form_data = {
            'heading': heading,
            'subheading': subheading,
            'button_text': button_text,
            'description': description
        }
        log_hero_change(session['admin_username'], hero, form_data)
        
        hero.heading = heading
        hero.subheading = subheading
        hero.button_text = button_text
        hero.description = description
        db.session.commit()
        
        flash("Hero section updated successfully!", "success")
        return redirect(url_for('admin_dashboard', tab='hero'))
        
    return render_template(
        "dashboard.html", 
        hero=hero, 
        principal_cards=principal_cards, 
        facilities=facilities, 
        vision=vision, 
        value_cards=value_cards,
        about_config=about_config,
        about_values=about_values,
        about_achievements=about_achievements,
        notices=notices,
        events=events,
        calendar=calendar,
        queries=queries,
        admission_setting=admission_setting,
        admission_subjects=admission_subjects,
        admission_documents=admission_documents,
        admission_queries=admission_queries,
        admission_config=admission_config,
        contact_config=contact_config,
        faqs=faqs,
        gallery_config=gallery_config,
        gallery_photos=gallery_photos,
        gallery_videos=gallery_videos,
        gallery_categories=gallery_categories,
        academics_config=academics_config,
        academics_curriculum_cards=academics_curriculum_cards,
        toppers=toppers,
        birthdays=birthdays,
        active_tab=active_tab, 
        logs=logs
    )


@app.route("/admin/principal/update/<card_id>", methods=['POST'])
def admin_update_principal_card(card_id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    card = PrincipalCard.query.filter_by(card_id=card_id).first_or_404()
    
    title = request.form.get('title', '').strip()
    subtitle = request.form.get('subtitle', '').strip()
    message_heading = request.form.get('message_heading', '').strip()
    message_p1 = request.form.get('message_p1', '').strip()
    message_p2 = request.form.get('message_p2', '').strip()
    signature_name = request.form.get('signature_name', '').strip()
    signature_role = request.form.get('signature_role', '').strip()
    
    image_url = card.image_url
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded_filename = save_uploaded_file(file)
            if uploaded_filename:
                image_url = uploaded_filename
            else:
                flash("Invalid image file format.", "error")
                return redirect(url_for('admin_dashboard', tab='principal'))
    
    if not all([title, subtitle, image_url, message_heading, message_p1, message_p2, signature_name, signature_role]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='principal'))
        
    form_data = {
        'title': title,
        'subtitle': subtitle,
        'image_url': image_url,
        'message_heading': message_heading,
        'message_p1': message_p1,
        'message_p2': message_p2,
        'signature_name': signature_name,
        'signature_role': signature_role
    }
    
    log_principal_change(session['admin_username'], card_id, card, form_data)
    
    card.title = title
    card.subtitle = subtitle
    card.image_url = image_url
    card.message_heading = message_heading
    card.message_p1 = message_p1
    card.message_p2 = message_p2
    card.signature_name = signature_name
    card.signature_role = signature_role
    db.session.commit()
    
    flash("Principal/Director card updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='principal'))

@app.route("/admin/facilities/add", methods=['POST'])
def admin_add_facility():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    icon = request.form.get('icon', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    link = request.form.get('link', '').strip()
    
    if not all([icon, title, description, link]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='facilities'))
        
    facility = Facility(icon=icon, title=title, description=description, link=link)
    db.session.add(facility)
    db.session.commit()
    
    log_facility_change(session['admin_username'], 'Added', title, icon)
    
    flash("Facility card added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='facilities'))

@app.route("/admin/facilities/edit/<int:id>", methods=['POST'])
def admin_edit_facility(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    facility = Facility.query.get_or_404(id)
    
    icon = request.form.get('icon', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    link = request.form.get('link', '').strip()
    
    if not all([icon, title, description, link]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='facilities'))
        
    facility.icon = icon
    facility.title = title
    facility.description = description
    facility.link = link
    db.session.commit()
    
    log_facility_change(session['admin_username'], 'Updated', title)
    
    flash("Facility card updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='facilities'))

@app.route("/admin/facilities/delete/<int:id>", methods=['POST'])
def admin_delete_facility(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    facility = Facility.query.get_or_404(id)
    title = facility.title
    db.session.delete(facility)
    db.session.commit()
    
    log_facility_change(session['admin_username'], 'Deleted', title)
    
    flash("Facility card deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='facilities'))

@app.route("/admin/values/add", methods=['POST'])
def admin_add_value():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    number = request.form.get('number', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded_filename = save_uploaded_file(file)
            if uploaded_filename:
                image_url = uploaded_filename
            else:
                flash("Invalid image file format.", "error")
                return redirect(url_for('admin_dashboard', tab='values'))
                
    if not all([title, description, image_url]):
        flash("Title, description, and image file are required.", "error")
        return redirect(url_for('admin_dashboard', tab='values'))
        
    value_card = ValueCard(number=number or None, title=title, description=description, image_url=image_url)
    db.session.add(value_card)
    db.session.commit()
    
    log_value_change(session['admin_username'], 'Added', title, number)
    
    flash("Value card added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='values'))

@app.route("/admin/values/edit/<int:id>", methods=['POST'])
def admin_edit_value(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    value_card = ValueCard.query.get_or_404(id)
    
    number = request.form.get('number', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    image_url = value_card.image_url
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded_filename = save_uploaded_file(file)
            if uploaded_filename:
                image_url = uploaded_filename
            else:
                flash("Invalid image file format.", "error")
                return redirect(url_for('admin_dashboard', tab='values'))
                
    if not all([title, description, image_url]):
        flash("Title, description, and image are required.", "error")
        return redirect(url_for('admin_dashboard', tab='values'))
        
    value_card.number = number or None
    value_card.title = title
    value_card.description = description
    value_card.image_url = image_url
    db.session.commit()
    
    log_value_change(session['admin_username'], 'Updated', title)
    
    flash("Value card updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='values'))

@app.route("/admin/values/delete/<int:id>", methods=['POST'])
def admin_delete_value(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    value_card = ValueCard.query.get_or_404(id)
    title = value_card.title
    db.session.delete(value_card)
    db.session.commit()
    
    log_value_change(session['admin_username'], 'Deleted', title)
    
    flash("Value card deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='values'))

@app.route("/admin/update-credentials", methods=['POST'])
def admin_update_credentials():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    current_username = session['admin_username']
    admin = Admin.query.filter_by(username=current_username).first()
    if not admin:
        flash("Admin account not found.", "error")
        return redirect(url_for('admin_dashboard', tab='credentials'))
        
    new_username = request.form.get('new_username', '').strip()
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    if not new_username or not current_password:
        flash("Username and current password are required.", "error")
        return redirect(url_for('admin_dashboard', tab='credentials'))
        
    if not admin.check_password(current_password):
        flash("Invalid current password.", "error")
        return redirect(url_for('admin_dashboard', tab='credentials'))
        
    if new_password:
        if new_password != confirm_password:
            flash("New passwords do not match.", "error")
            return redirect(url_for('admin_dashboard', tab='credentials'))
        admin.set_password(new_password)
        
    old_username = admin.username
    admin.username = new_username
    session['admin_username'] = new_username
    db.session.commit()
    
    log_credential_change(new_username, old_username)
    
    flash("Credentials updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='credentials'))

@app.route("/admin/vision/update", methods=['POST'])
def admin_update_vision():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    vision = VisionContent.query.first()
    if not vision:
        vision = VisionContent(
            label='OUR VISION',
            heading='Shaping Future Leaders Through Excellence in Education',
            p1='Paragraph 1 default',
            p2='Paragraph 2 default',
            p3='Paragraph 3 default'
        )
        db.session.add(vision)
        db.session.commit()
        
    label = request.form.get('label', '').strip()
    heading = request.form.get('heading', '').strip()
    p1 = request.form.get('p1', '').strip()
    p2 = request.form.get('p2', '').strip()
    p3 = request.form.get('p3', '').strip()
    
    if not all([label, heading, p1, p2, p3]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='vision'))
        
    form_data = {
        'label': label,
        'heading': heading,
        'p1': p1,
        'p2': p2,
        'p3': p3
    }
    
    log_vision_change(session['admin_username'], vision, form_data)
    
    vision.label = label
    vision.heading = heading
    vision.p1 = p1
    vision.p2 = p2
    vision.p3 = p3
    db.session.commit()
    
    flash("Vision section updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='vision'))

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('admin_login'))

@app.route("/admin/about/update/hero", methods=['POST'])
def admin_update_about_hero():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    eyebrow = request.form.get('hero_eyebrow', '').strip()
    heading = request.form.get('hero_heading', '').strip()
    description = request.form.get('hero_description', '').strip()
    
    if not all([eyebrow, heading, description]):
        flash("All hero fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_content'))
        
    old_data = {
        'hero_eyebrow': config.hero_eyebrow,
        'hero_heading': config.hero_heading,
        'hero_description': config.hero_description
    }
    form_data = {
        'hero_eyebrow': eyebrow,
        'hero_heading': heading,
        'hero_description': description
    }
    
    log_about_content_change(session['admin_username'], 'Hero', old_data, form_data)
    
    config.hero_eyebrow = eyebrow
    config.hero_heading = heading
    config.hero_description = description
    db.session.commit()
    
    flash("About Page Hero updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_content'))

@app.route("/admin/about/update/who", methods=['POST'])
def admin_update_about_who():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    eyebrow = request.form.get('who_eyebrow', '').strip()
    heading = request.form.get('who_heading', '').strip()
    p1 = request.form.get('who_p1', '').strip()
    p2 = request.form.get('who_p2', '').strip()
    
    image_url = config.who_image_url
    if 'who_image' in request.files:
        file = request.files['who_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='about_content'))
                
    if not all([eyebrow, heading, p1, p2, image_url]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_content'))
        
    old_data = {
        'who_eyebrow': config.who_eyebrow,
        'who_heading': config.who_heading,
        'who_p1': config.who_p1,
        'who_p2': config.who_p2,
        'who_image_url': config.who_image_url
    }
    form_data = {
        'who_eyebrow': eyebrow,
        'who_heading': heading,
        'who_p1': p1,
        'who_p2': p2,
        'who_image_url': image_url
    }
    
    log_about_content_change(session['admin_username'], 'Who We Are', old_data, form_data)
    
    config.who_eyebrow = eyebrow
    config.who_heading = heading
    config.who_p1 = p1
    config.who_p2 = p2
    config.who_image_url = image_url
    db.session.commit()
    
    flash("Who We Are section updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_content'))

@app.route("/admin/about/update/history", methods=['POST'])
def admin_update_about_history():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    eyebrow = request.form.get('history_eyebrow', '').strip()
    heading = request.form.get('history_heading', '').strip()
    p1 = request.form.get('history_p1', '').strip()
    p2 = request.form.get('history_p2', '').strip()
    
    image_url = config.history_image_url
    if 'history_image' in request.files:
        file = request.files['history_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='about_content'))
                
    if not all([eyebrow, heading, p1, p2, image_url]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_content'))
        
    old_data = {
        'history_eyebrow': config.history_eyebrow,
        'history_heading': config.history_heading,
        'history_p1': config.history_p1,
        'history_p2': config.history_p2,
        'history_image_url': config.history_image_url
    }
    form_data = {
        'history_eyebrow': eyebrow,
        'history_heading': heading,
        'history_p1': p1,
        'history_p2': p2,
        'history_image_url': image_url
    }
    
    log_about_content_change(session['admin_username'], 'History', old_data, form_data)
    
    config.history_eyebrow = eyebrow
    config.history_heading = heading
    config.history_p1 = p1
    config.history_p2 = p2
    config.history_image_url = image_url
    db.session.commit()
    
    flash("History section updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_content'))

@app.route("/admin/about/update/vm", methods=['POST'])
def admin_update_about_vm():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    eyebrow = request.form.get('vm_eyebrow', '').strip()
    heading = request.form.get('vm_heading', '').strip()
    vision_title = request.form.get('vm_vision_title', '').strip()
    vision_desc = request.form.get('vm_vision_desc', '').strip()
    mission_title = request.form.get('vm_mission_title', '').strip()
    mission_bullets = request.form.get('vm_mission_bullets', '').strip()
    
    if not all([eyebrow, heading, vision_title, vision_desc, mission_title, mission_bullets]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_content'))
        
    old_data = {
        'vm_eyebrow': config.vm_eyebrow,
        'vm_heading': config.vm_heading,
        'vm_vision_title': config.vm_vision_title,
        'vm_vision_desc': config.vm_vision_desc,
        'vm_mission_title': config.vm_mission_title,
        'vm_mission_bullets': config.vm_mission_bullets
    }
    form_data = {
        'vm_eyebrow': eyebrow,
        'vm_heading': heading,
        'vm_vision_title': vision_title,
        'vm_vision_desc': vision_desc,
        'vm_mission_title': mission_title,
        'vm_mission_bullets': mission_bullets
    }
    
    log_about_content_change(session['admin_username'], 'Vision & Mission', old_data, form_data)
    
    config.vm_eyebrow = eyebrow
    config.vm_heading = heading
    config.vm_vision_title = vision_title
    config.vm_vision_desc = vision_desc
    config.vm_mission_title = mission_title
    config.vm_mission_bullets = mission_bullets
    db.session.commit()
    
    flash("Vision & Mission section updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_content'))

@app.route("/admin/about/update/mgmt", methods=['POST'])
def admin_update_about_mgmt():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    eyebrow = request.form.get('mgmt_eyebrow', '').strip()
    heading = request.form.get('mgmt_heading', '').strip()
    p1 = request.form.get('mgmt_p1', '').strip()
    p2 = request.form.get('mgmt_p2', '').strip()
    
    image_url = config.mgmt_image_url
    if 'mgmt_image' in request.files:
        file = request.files['mgmt_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='about_content'))
                
    if not all([eyebrow, heading, p1, p2, image_url]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_content'))
        
    old_data = {
        'mgmt_eyebrow': config.mgmt_eyebrow,
        'mgmt_heading': config.mgmt_heading,
        'mgmt_p1': config.mgmt_p1,
        'mgmt_p2': config.mgmt_p2,
        'mgmt_image_url': config.mgmt_image_url
    }
    form_data = {
        'mgmt_eyebrow': eyebrow,
        'mgmt_heading': heading,
        'mgmt_p1': p1,
        'mgmt_p2': p2,
        'mgmt_image_url': image_url
    }
    
    log_about_content_change(session['admin_username'], 'Management', old_data, form_data)
    
    config.mgmt_eyebrow = eyebrow
    config.mgmt_heading = heading
    config.mgmt_p1 = p1
    config.mgmt_p2 = p2
    config.mgmt_image_url = image_url
    db.session.commit()
    
    flash("Management section updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_content'))

@app.route("/admin/about/update/principal", methods=['POST'])
def admin_update_about_principal():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    eyebrow = request.form.get('principal_eyebrow', '').strip()
    heading = request.form.get('principal_heading', '').strip()
    p1 = request.form.get('principal_p1', '').strip()
    p2 = request.form.get('principal_p2', '').strip()
    p3 = request.form.get('principal_p3', '').strip()
    signature_name = request.form.get('principal_signature_name', '').strip()
    signature_role = request.form.get('principal_signature_role', '').strip()
    
    image_url = config.principal_image_url
    if 'principal_image' in request.files:
        file = request.files['principal_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='about_content'))
                
    if not all([eyebrow, heading, p1, p2, p3, signature_name, signature_role, image_url]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_content'))
        
    old_data = {
        'principal_eyebrow': config.principal_eyebrow,
        'principal_heading': config.principal_heading,
        'principal_p1': config.principal_p1,
        'principal_p2': config.principal_p2,
        'principal_p3': config.principal_p3,
        'principal_signature_name': config.principal_signature_name,
        'principal_signature_role': config.principal_signature_role,
        'principal_image_url': config.principal_image_url
    }
    form_data = {
        'principal_eyebrow': eyebrow,
        'principal_heading': heading,
        'principal_p1': p1,
        'principal_p2': p2,
        'principal_p3': p3,
        'principal_signature_name': signature_name,
        'principal_signature_role': signature_role,
        'principal_image_url': image_url
    }
    
    log_about_content_change(session['admin_username'], 'Principal Message', old_data, form_data)
    
    config.principal_eyebrow = eyebrow
    config.principal_heading = heading
    config.principal_p1 = p1
    config.principal_p2 = p2
    config.principal_p3 = p3
    config.principal_signature_name = signature_name
    config.principal_signature_role = signature_role
    config.principal_image_url = image_url
    db.session.commit()
    
    flash("Principal Message updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_content'))

@app.route("/admin/about/update/banner", methods=['POST'])
def admin_update_about_banner():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    config = AboutPageConfig.query.first()
    
    image_url = config.achievements_banner_url
    if 'banner_image' in request.files:
        file = request.files['banner_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='about_achievements'))
                
    old_data = {'achievements_banner_url': config.achievements_banner_url}
    form_data = {'achievements_banner_url': image_url}
    
    log_about_content_change(session['admin_username'], 'Achievements Banner', old_data, form_data)
    
    config.achievements_banner_url = image_url
    db.session.commit()
    
    flash("Achievements bottom banner updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_achievements'))

@app.route("/admin/about/values/add", methods=['POST'])
def admin_add_about_value():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    icon_svg = request.form.get('icon_svg', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if not all([icon_svg, title, description]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_values'))
        
    val = AboutPageValue(icon_svg=icon_svg, title=title, description=description)
    db.session.add(val)
    db.session.commit()
    
    log_about_value_change(session['admin_username'], 'Added', title)
    flash("About value added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_values'))

@app.route("/admin/about/values/edit/<int:id>", methods=['POST'])
def admin_edit_about_value(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    val = AboutPageValue.query.get_or_404(id)
    icon_svg = request.form.get('icon_svg', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if not all([icon_svg, title, description]):
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_values'))
        
    val.icon_svg = icon_svg
    val.title = title
    val.description = description
    db.session.commit()
    
    log_about_value_change(session['admin_username'], 'Updated', title)
    flash("About value updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_values'))

@app.route("/admin/about/values/delete/<int:id>", methods=['POST'])
def admin_delete_about_value(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    val = AboutPageValue.query.get_or_404(id)
    title = val.title
    db.session.delete(val)
    db.session.commit()
    
    log_about_value_change(session['admin_username'], 'Deleted', title)
    flash("About value deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_values'))

@app.route("/admin/about/achievements/add", methods=['POST'])
def admin_add_about_achievement():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    text = request.form.get('text', '').strip()
    
    if not text:
        flash("Achievement text is required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_achievements'))
        
    ach = AboutPageAchievement(text=text)
    db.session.add(ach)
    db.session.commit()
    
    log_about_achievement_change(session['admin_username'], 'Added', text)
    flash("Achievement added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_achievements'))

@app.route("/admin/about/achievements/edit/<int:id>", methods=['POST'])
def admin_edit_about_achievement(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    ach = AboutPageAchievement.query.get_or_404(id)
    text = request.form.get('text', '').strip()
    
    if not text:
        flash("Achievement text is required.", "error")
        return redirect(url_for('admin_dashboard', tab='about_achievements'))
        
    ach.text = text
    db.session.commit()
    
    log_about_achievement_change(session['admin_username'], 'Updated', text)
    flash("Achievement updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_achievements'))

@app.route("/admin/about/achievements/delete/<int:id>", methods=['POST'])
def admin_delete_about_achievement(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
    ach = AboutPageAchievement.query.get_or_404(id)
    text = ach.text
    db.session.delete(ach)
    db.session.commit()
    
    log_about_achievement_change(session['admin_username'], 'Deleted', text)
    flash("Achievement deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='about_achievements'))

@app.route("/about")
def about_us():
    about_config = AboutPageConfig.query.first()
    about_values = AboutPageValue.query.all()
    about_achievements = AboutPageAchievement.query.all()
    return render_template(
        "about.html",
        about_config=about_config,
        about_values=about_values,
        about_achievements=about_achievements,
        name="About"
    )
@app.route("/academics")
def academics_page():
    config = AcademicsPageConfig.query.first()
    if not config:
        config = AcademicsPageConfig()
        db.session.add(config)
        db.session.commit()
    curriculum_cards = AcademicsCurriculumCard.query.order_by(AcademicsCurriculumCard.id.asc()).all()
    toppers = AcademicTopper.query.order_by(AcademicTopper.id.asc()).all()
    return render_template(
        'academics.html',
        name="Academics",
        config=config,
        curriculum_cards=curriculum_cards,
        toppers=toppers
    )

@app.route("/contact-us", methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email_val = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        if not first_name or not last_name or not email_val or not subject or not message:
            return {"success": False, "error": "All fields except phone number are required."}, 400
            
        new_query = ContactQuery(
            first_name=first_name,
            last_name=last_name,
            email=email_val,
            phone=phone,
            subject=subject,
            message=message
        )
        db.session.add(new_query)
        db.session.commit()
        
        # Send dynamic HTML email notification
        try:
            msg = html_email_fetcher()
            email_err = email_sender(email_function.email, email_function.reciever, msg)
            if email_err:
                app.logger.error(email_err)
        except Exception as e:
            app.logger.error(f"Email notification failed: {e}")
            
        return {"success": True}

    contact_config = ContactPageConfig.query.first()
    if not contact_config:
        contact_config = ContactPageConfig()
        db.session.add(contact_config)
        db.session.commit()
    faqs = FAQItem.query.order_by(FAQItem.id.asc()).all()
    return render_template(
        'contact.html',
        name="Contact-us",
        contact_config=contact_config,
        faqs=faqs
    )



@app.route("/admin/queries/delete/<int:id>", methods=['POST'])
def admin_delete_query(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    query = ContactQuery.query.get_or_404(id)
    db.session.delete(query)
    db.session.commit()
    flash("Query deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='queries'))    
@app.route("/admin/notice/add", methods=['POST'])
def admin_add_notice():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    category = request.form.get('category', '').strip()
    date = request.form.get('date', '').strip()
    title = request.form.get('title', '').strip()
    target = request.form.get('target', '').strip()
    content = request.form.get('content', '').strip()
    issued_by = request.form.get('issued_by', '').strip()
    
    if not category or not date or not title or not target or not content or not issued_by:
        flash("All notice fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='events_notices'))
        
    notice = Notice(
        category=category,
        date=date,
        title=title,
        target=target,
        content=content,
        issued_by=issued_by
    )
    db.session.add(notice)
    db.session.commit()
    
    log_notice_change(session['admin_username'], 'Added', title, category)
    flash("Notice card added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='events_notices'))

@app.route("/admin/notice/edit/<int:id>", methods=['POST'])
def admin_edit_notice(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    notice = Notice.query.get_or_404(id)
    
    category = request.form.get('category', '').strip()
    date = request.form.get('date', '').strip()
    title = request.form.get('title', '').strip()
    target = request.form.get('target', '').strip()
    content = request.form.get('content', '').strip()
    issued_by = request.form.get('issued_by', '').strip()
    
    if not category or not date or not title or not target or not content or not issued_by:
        flash("All notice fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='events_notices'))
        
    notice.category = category
    notice.date = date
    notice.title = title
    notice.target = target
    notice.content = content
    notice.issued_by = issued_by
    db.session.commit()
    
    log_notice_change(session['admin_username'], 'Updated', title, category)
    flash("Notice card updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='events_notices'))

@app.route("/admin/notice/delete/<int:id>", methods=['POST'])
def admin_delete_notice(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    notice = Notice.query.get_or_404(id)
    title = notice.title
    category = notice.category
    
    db.session.delete(notice)
    db.session.commit()
    
    log_notice_change(session['admin_username'], 'Deleted', title, category)
    flash("Notice card deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='events_notices'))

@app.route("/admin/event/add", methods=['POST'])
def admin_add_event():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    title = request.form.get('title', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()
    video_url = request.form.get('video_url', '').strip()
    tags = request.form.get('tags', '').strip()
    
    # Handle image uploads or fallback to text box URL inputs
    image1_url = ""
    if 'image1' in request.files:
        file = request.files['image1']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image1_url = uploaded
    if not image1_url:
        image1_url = request.form.get('image1_url_text', '').strip() or "placeholder.jpg"
        
    image2_url = ""
    if 'image2' in request.files:
        file = request.files['image2']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image2_url = uploaded
    if not image2_url:
        image2_url = request.form.get('image2_url_text', '').strip() or "placeholder.jpg"
        
    video_thumb_url = ""
    if 'video_thumb' in request.files:
        file = request.files['video_thumb']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                video_thumb_url = uploaded
    if not video_thumb_url:
        video_thumb_url = request.form.get('video_thumb_url_text', '').strip() or "placeholder.jpg"
        
    if not title or not date or not description:
        flash("Title, Date, and Description are required.", "error")
        return redirect(url_for('admin_dashboard', tab='events_crud'))
        
    event = Event(
        title=title,
        date=date,
        description=description,
        image1_url=image1_url,
        image2_url=image2_url,
        video_url=video_url,
        video_thumb_url=video_thumb_url,
        tags=tags
    )
    db.session.add(event)
    db.session.commit()
    
    log_event_change(session['admin_username'], 'Added', title)
    flash("Event card added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='events_crud'))

@app.route("/admin/event/edit/<int:id>", methods=['POST'])
def admin_edit_event(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    event = Event.query.get_or_404(id)
    
    title = request.form.get('title', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()
    video_url = request.form.get('video_url', '').strip()
    tags = request.form.get('tags', '').strip()
    
    # Handle image updates
    image1_url = event.image1_url
    if 'image1' in request.files:
        file = request.files['image1']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image1_url = uploaded
    if request.form.get('image1_url_text', '').strip():
        image1_url = request.form.get('image1_url_text', '').strip()
        
    image2_url = event.image2_url
    if 'image2' in request.files:
        file = request.files['image2']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image2_url = uploaded
    if request.form.get('image2_url_text', '').strip():
        image2_url = request.form.get('image2_url_text', '').strip()
        
    video_thumb_url = event.video_thumb_url
    if 'video_thumb' in request.files:
        file = request.files['video_thumb']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                video_thumb_url = uploaded
    if request.form.get('video_thumb_url_text', '').strip():
        video_thumb_url = request.form.get('video_thumb_url_text', '').strip()
        
    if not title or not date or not description:
        flash("Title, Date, and Description are required.", "error")
        return redirect(url_for('admin_dashboard', tab='events_crud'))
        
    event.title = title
    event.date = date
    event.description = description
    event.image1_url = image1_url
    event.image2_url = image2_url
    event.video_url = video_url
    event.video_thumb_url = video_thumb_url
    event.tags = tags
    db.session.commit()
    
    log_event_change(session['admin_username'], 'Updated', title)
    flash("Event updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='events_crud'))

@app.route("/admin/event/delete/<int:id>", methods=['POST'])
def admin_delete_event(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    event = Event.query.get_or_404(id)
    title = event.title
    
    db.session.delete(event)
    db.session.commit()
    
    log_event_change(session['admin_username'], 'Deleted', title)
    flash("Event deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='events_crud'))

@app.route("/admin/calendar/update", methods=['POST'])
def admin_update_calendar():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    calendar = AcademicCalendar.query.first()
    if not calendar:
        calendar = AcademicCalendar(image_url="Annual_planner.png")
        db.session.add(calendar)
        db.session.commit()
        
    old_url = calendar.image_url
    image_url = old_url
    
    # Handle image uploads
    if 'calendar_img' in request.files:
        file = request.files['calendar_img']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
                
    text_url = request.form.get('calendar_img_url_text', '').strip()
    if text_url:
        image_url = text_url
        
    calendar.image_url = image_url
    db.session.commit()
    
    log_calendar_change(session['admin_username'], old_url, image_url)
    flash("Academic Calendar updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='calendar'))

@app.route("/events-&-notices")
def events_and_notices():
    notices = Notice.query.order_by(Notice.id.desc()).all()
    events = Event.query.order_by(Event.id.desc()).all()
    calendar = AcademicCalendar.query.first()
    if not calendar:
        calendar = AcademicCalendar(image_url="Annual_planner.png")
        db.session.add(calendar)
        db.session.commit()
    return render_template(
        'events-notices.html',
        name="Events and Notices",
        notices=notices,
        events=events,
        calendar=calendar
    )

@app.route("/admission", methods=['GET', 'POST'])
def admission_page():
    if request.method == 'POST':
        setting = AdmissionSetting.query.first()
        if not setting or not setting.admissions_open:
            return {"success": False, "error": "Admissions are currently closed."}, 400
            
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        dob = request.form.get('dob', '').strip()
        class_applying = request.form.get('classApplying', '').strip()
        parent_name = request.form.get('parentName', '').strip()
        relationship = request.form.get('relationship', '').strip()
        phone = request.form.get('phone', '').strip()
        email_val = request.form.get('email', '').strip()
        prev_school = request.form.get('prevSchool', '').strip()
        message = request.form.get('message', '').strip()
        
        if not first_name or not last_name or not dob or not class_applying or not parent_name or not relationship or not phone or not email_val:
            return {"success": False, "error": "All required fields must be completed."}, 400
            
        new_query = AdmissionQuery(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            class_applying=class_applying,
            parent_name=parent_name,
            relationship=relationship,
            phone=phone,
            email=email_val,
            prev_school=prev_school,
            message=message
        )
        db.session.add(new_query)
        db.session.commit()
        
        # Send dynamic HTML email notification
        try:
            msg = html_admission_email_fetcher()
            email_err = email_sender(email_function.email, email_function.reciever, msg)
            if email_err:
                app.logger.error(email_err)
        except Exception as e:
            app.logger.error(f"Email notification failed: {e}")
            
        return {"success": True}
        
    setting = AdmissionSetting.query.first()
    subjects = SubjectItem.query.all()
    documents = DocItem.query.all()
    admission_config = AdmissionPageConfig.query.first()
    if not admission_config:
        admission_config = AdmissionPageConfig()
        db.session.add(admission_config)
        db.session.commit()
    return render_template('admission.html',
                           name="Admissions",
                           setting=setting,
                           subjects=subjects,
                           documents=documents,
                           admission_config=admission_config
                           )


# ----------------------------------------------------
# CONTACT & FAQ CONTROLS ROUTES
# ----------------------------------------------------

@app.route("/admin/contact/info", methods=['POST'])
def admin_contact_info():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    config = ContactPageConfig.query.first()
    if not config:
        config = ContactPageConfig()
        db.session.add(config)
        
    form_data = {
        'address_line1': request.form.get('address_line1', '').strip(),
        'address_line2': request.form.get('address_line2', '').strip(),
        'phone1': request.form.get('phone1', '').strip(),
        'phone2': request.form.get('phone2', '').strip(),
        'email1': request.form.get('email1', '').strip(),
        'email2': request.form.get('email2', '').strip(),
        'whatsapp': request.form.get('whatsapp', '').strip()
    }
    
    if not all(form_data.values()):
        flash("All Contact Info fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='contact_settings'))
        
    log_contact_config_change(session['admin_username'], config, form_data)
    
    config.address_line1 = form_data['address_line1']
    config.address_line2 = form_data['address_line2']
    config.phone1 = form_data['phone1']
    config.phone2 = form_data['phone2']
    config.email1 = form_data['email1']
    config.email2 = form_data['email2']
    config.whatsapp = form_data['whatsapp']
    
    db.session.commit()
    flash("Contact details updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='contact_settings'))


@app.route("/admin/contact/timings", methods=['POST'])
def admin_contact_timings():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    config = ContactPageConfig.query.first()
    if not config:
        config = ContactPageConfig()
        db.session.add(config)
        
    form_data = {
        'office_hours_mon_fri': request.form.get('office_hours_mon_fri', '').strip(),
        'office_hours_sat': request.form.get('office_hours_sat', '').strip(),
        'office_hours_sun': request.form.get('office_hours_sun', '').strip(),
        'school_hours_primary': request.form.get('school_hours_primary', '').strip(),
        'school_hours_middle': request.form.get('school_hours_middle', '').strip(),
        'school_hours_senior': request.form.get('school_hours_senior', '').strip(),
        'admission_hours_mon_sat': request.form.get('admission_hours_mon_sat', '').strip(),
        'admission_hours_sun': request.form.get('admission_hours_sun', '').strip(),
        'admission_hours_note': request.form.get('admission_hours_note', '').strip()
    }
    
    if not all(form_data.values()):
        flash("All timing fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='contact_settings'))
        
    log_contact_config_change(session['admin_username'], config, form_data)
    
    config.office_hours_mon_fri = form_data['office_hours_mon_fri']
    config.office_hours_sat = form_data['office_hours_sat']
    config.office_hours_sun = form_data['office_hours_sun']
    config.school_hours_primary = form_data['school_hours_primary']
    config.school_hours_middle = form_data['school_hours_middle']
    config.school_hours_senior = form_data['school_hours_senior']
    config.admission_hours_mon_sat = form_data['admission_hours_mon_sat']
    config.admission_hours_sun = form_data['admission_hours_sun']
    config.admission_hours_note = form_data['admission_hours_note']
    
    db.session.commit()
    flash("School timings updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='contact_settings'))


@app.route("/admin/contact/faqs/add", methods=['POST'])
def admin_add_faq():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()
    
    if not question or not answer:
        flash("FAQ question and answer are required.", "error")
        return redirect(url_for('admin_dashboard', tab='contact_faqs'))
        
    new_faq = FAQItem(question=question, answer=answer)
    db.session.add(new_faq)
    db.session.commit()
    
    log_faq_change(session['admin_username'], 'Added', question)
    flash("FAQ added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='contact_faqs'))


@app.route("/admin/contact/faqs/edit/<int:id>", methods=['POST'])
def admin_edit_faq(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    faq = FAQItem.query.get_or_404(id)
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()
    
    if not question or not answer:
        flash("FAQ question and answer are required.", "error")
        return redirect(url_for('admin_dashboard', tab='contact_faqs'))
        
    faq.question = question
    faq.answer = answer
    db.session.commit()
    
    log_faq_change(session['admin_username'], 'Updated', question)
    flash("FAQ updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='contact_faqs'))


@app.route("/admin/contact/faqs/delete/<int:id>", methods=['POST'])
def admin_delete_faq(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    faq = FAQItem.query.get_or_404(id)
    question = faq.question
    db.session.delete(faq)
    db.session.commit()
    
    log_faq_change(session['admin_username'], 'Deleted', question)
    flash("FAQ deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='contact_faqs'))


# ----------------------------------------------------
# ADMISSION CONTROLS ROUTES
# ----------------------------------------------------

@app.route("/admin/admission/settings", methods=['POST'])
def admin_admission_settings():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    setting = AdmissionSetting.query.first()
    if not setting:
        setting = AdmissionSetting()
        db.session.add(setting)
        
    admissions_open = request.form.get('admissions_open') == 'true'
    closed_message_heading = request.form.get('closed_message_heading', '').strip()
    closed_message_body = request.form.get('closed_message_body', '').strip()
    
    if not closed_message_heading or not closed_message_body:
        flash("Message heading and body are required when admissions are closed.", "error")
        return redirect(url_for('admin_dashboard', tab='admission_settings'))
        
    form_data = {
        'admissions_open': admissions_open,
        'closed_message_heading': closed_message_heading,
        'closed_message_body': closed_message_body
    }
    
    log_admission_setting_change(session['admin_username'], setting, form_data)
    
    setting.admissions_open = admissions_open
    setting.closed_message_heading = closed_message_heading
    setting.closed_message_body = closed_message_body
    db.session.commit()
    
    flash("Admission settings updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_settings'))


@app.route("/admin/admission/subjects/add", methods=['POST'])
def admin_add_subject():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    title = request.form.get('title', '').strip()
    svg_icon = request.form.get('svg_icon', '').strip()
    
    if not title or not svg_icon:
        flash("Subject title and icon are required.", "error")
        return redirect(url_for('admin_dashboard', tab='admission_subjects'))
        
    new_subject = SubjectItem(title=title, svg_icon=svg_icon)
    db.session.add(new_subject)
    db.session.commit()
    
    log_subject_change(session['admin_username'], 'Added', title)
    flash("Test subject added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_subjects'))


@app.route("/admin/admission/subjects/edit/<int:id>", methods=['POST'])
def admin_edit_subject(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    subject = SubjectItem.query.get_or_404(id)
    title = request.form.get('title', '').strip()
    svg_icon = request.form.get('svg_icon', '').strip()
    
    if not title or not svg_icon:
        flash("Subject title and icon are required.", "error")
        return redirect(url_for('admin_dashboard', tab='admission_subjects'))
        
    subject.title = title
    subject.svg_icon = svg_icon
    db.session.commit()
    
    log_subject_change(session['admin_username'], 'Updated', title)
    flash("Test subject updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_subjects'))


@app.route("/admin/admission/subjects/delete/<int:id>", methods=['POST'])
def admin_delete_subject(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    subject = SubjectItem.query.get_or_404(id)
    title = subject.title
    db.session.delete(subject)
    db.session.commit()
    
    log_subject_change(session['admin_username'], 'Deleted', title)
    flash("Test subject deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_subjects'))


@app.route("/admin/admission/documents/add", methods=['POST'])
def admin_add_document():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    name = request.form.get('name', '').strip()
    note = request.form.get('note', '').strip()
    svg_icon = request.form.get('svg_icon', '').strip()
    
    if not name or not note or not svg_icon:
        flash("Document name, note, and icon are required.", "error")
        return redirect(url_for('admin_dashboard', tab='admission_documents'))
        
    new_doc = DocItem(name=name, note=note, svg_icon=svg_icon)
    db.session.add(new_doc)
    db.session.commit()
    
    log_document_change(session['admin_username'], 'Added', name)
    flash("Required document added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_documents'))


@app.route("/admin/admission/documents/edit/<int:id>", methods=['POST'])
def admin_edit_document(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    doc = DocItem.query.get_or_404(id)
    name = request.form.get('name', '').strip()
    note = request.form.get('note', '').strip()
    svg_icon = request.form.get('svg_icon', '').strip()
    
    if not name or not note or not svg_icon:
        flash("Document name, note, and icon are required.", "error")
        return redirect(url_for('admin_dashboard', tab='admission_documents'))
        
    doc.name = name
    doc.note = note
    doc.svg_icon = svg_icon
    db.session.commit()
    
    log_document_change(session['admin_username'], 'Updated', name)
    flash("Required document updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_documents'))


@app.route("/admin/admission/documents/delete/<int:id>", methods=['POST'])
def admin_delete_document(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    doc = DocItem.query.get_or_404(id)
    name = doc.name
    db.session.delete(doc)
    db.session.commit()
    
    log_document_change(session['admin_username'], 'Deleted', name)
    flash("Required document deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_documents'))


@app.route("/admin/admission/queries/delete/<int:id>", methods=['POST'])
def admin_delete_admission_query(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    query = AdmissionQuery.query.get_or_404(id)
    db.session.delete(query)
    db.session.commit()
    
    flash("Admission query deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='queries'))


@app.route("/admin/admission/content/update/<section>", methods=['POST'])
def admin_admission_content_update(section):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    config = AdmissionPageConfig.query.first()
    if not config:
        config = AdmissionPageConfig()
        db.session.add(config)
        
    form_data = {}
    if section == 'hero':
        form_data['hero_eyebrow'] = request.form.get('hero_eyebrow', '').strip()
        form_data['hero_heading'] = request.form.get('hero_heading', '').strip()
        form_data['hero_subheading'] = request.form.get('hero_subheading', '').strip()
        if not form_data['hero_eyebrow'] or not form_data['hero_heading'] or not form_data['hero_subheading']:
            flash("All Hero section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Hero', config, form_data)
        config.hero_eyebrow = form_data['hero_eyebrow']
        config.hero_heading = form_data['hero_heading']
        config.hero_subheading = form_data['hero_subheading']
        
    elif section == 'overview':
        form_data['overview_eyebrow'] = request.form.get('overview_eyebrow', '').strip()
        form_data['overview_heading'] = request.form.get('overview_heading', '').strip()
        form_data['overview_p1'] = request.form.get('overview_p1', '').strip()
        form_data['overview_p2'] = request.form.get('overview_p2', '').strip()
        if not form_data['overview_eyebrow'] or not form_data['overview_heading'] or not form_data['overview_p1'] or not form_data['overview_p2']:
            flash("All Overview section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Overview', config, form_data)
        config.overview_eyebrow = form_data['overview_eyebrow']
        config.overview_heading = form_data['overview_heading']
        config.overview_p1 = form_data['overview_p1']
        config.overview_p2 = form_data['overview_p2']
        
    elif section == 'visit':
        form_data['visit_title'] = request.form.get('visit_title', '').strip()
        form_data['visit_text'] = request.form.get('visit_text', '').strip()
        form_data['office_days'] = request.form.get('office_days', '').strip()
        form_data['office_hours'] = request.form.get('office_hours', '').strip()
        form_data['office_note'] = request.form.get('office_note', '').strip()
        if not form_data['visit_title'] or not form_data['visit_text'] or not form_data['office_days'] or not form_data['office_hours'] or not form_data['office_note']:
            flash("All Visit section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Visit', config, form_data)
        config.visit_title = form_data['visit_title']
        config.visit_text = form_data['visit_text']
        config.office_days = form_data['office_days']
        config.office_hours = form_data['office_hours']
        config.office_note = form_data['office_note']
        
    elif section == 'process':
        form_data['process_eyebrow'] = request.form.get('process_eyebrow', '').strip()
        form_data['process_heading'] = request.form.get('process_heading', '').strip()
        form_data['process_text'] = request.form.get('process_text', '').strip()
        if not form_data['process_eyebrow'] or not form_data['process_heading'] or not form_data['process_text']:
            flash("All Process section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Process', config, form_data)
        config.process_eyebrow = form_data['process_eyebrow']
        config.process_heading = form_data['process_heading']
        config.process_text = form_data['process_text']
        
    elif section == 'test':
        form_data['test_heading'] = request.form.get('test_heading', '').strip()
        form_data['test_p1'] = request.form.get('test_p1', '').strip()
        form_data['test_p2'] = request.form.get('test_p2', '').strip()
        form_data['test_p3'] = request.form.get('test_p3', '').strip()
        form_data['test_note'] = request.form.get('test_note', '').strip()
        if not form_data['test_heading'] or not form_data['test_p1'] or not form_data['test_p2'] or not form_data['test_p3'] or not form_data['test_note']:
            flash("All Test expectations section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Test Expectations', config, form_data)
        config.test_heading = form_data['test_heading']
        config.test_p1 = form_data['test_p1']
        config.test_p2 = form_data['test_p2']
        config.test_p3 = form_data['test_p3']
        config.test_note = form_data['test_note']
        
    elif section == 'steps':
        for i in range(1, 7):
            form_data[f'step{i}_title'] = request.form.get(f'step{i}_title', '').strip()
            form_data[f'step{i}_text'] = request.form.get(f'step{i}_text', '').strip()
            if not form_data[f'step{i}_title'] or not form_data[f'step{i}_text']:
                flash("All enrollment steps titles and descriptions are required.", "error")
                return redirect(url_for('admin_dashboard', tab='admission_content'))
                
        log_admission_content_change(session['admin_username'], 'Enrollment Steps Details', config, form_data)
        for i in range(1, 7):
            setattr(config, f'step{i}_title', form_data[f'step{i}_title'])
            setattr(config, f'step{i}_text', form_data[f'step{i}_text'])
            
    elif section == 'doc_info':
        form_data['doc_eyebrow'] = request.form.get('doc_eyebrow', '').strip()
        form_data['doc_heading'] = request.form.get('doc_heading', '').strip()
        form_data['doc_text'] = request.form.get('doc_text', '').strip()
        form_data['tc_notice_heading'] = request.form.get('tc_notice_heading', '').strip()
        form_data['tc_notice_text'] = request.form.get('tc_notice_text', '').strip()
        if not form_data['doc_eyebrow'] or not form_data['doc_heading'] or not form_data['doc_text'] or not form_data['tc_notice_heading'] or not form_data['tc_notice_text']:
            flash("All Required Documents section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Documents Section Info', config, form_data)
        config.doc_eyebrow = form_data['doc_eyebrow']
        config.doc_heading = form_data['doc_heading']
        config.doc_text = form_data['doc_text']
        config.tc_notice_heading = form_data['tc_notice_heading']
        config.tc_notice_text = form_data['tc_notice_text']
        
    elif section == 'ways':
        form_data['ways_eyebrow'] = request.form.get('ways_eyebrow', '').strip()
        form_data['ways_heading'] = request.form.get('ways_heading', '').strip()
        form_data['ways_text'] = request.form.get('ways_text', '').strip()
        form_data['way1_title'] = request.form.get('way1_title', '').strip()
        form_data['way1_text'] = request.form.get('way1_text', '').strip()
        form_data['way2_title'] = request.form.get('way2_title', '').strip()
        form_data['way2_text'] = request.form.get('way2_text', '').strip()
        if not form_data['ways_eyebrow'] or not form_data['ways_heading'] or not form_data['ways_text'] or not form_data['way1_title'] or not form_data['way1_text'] or not form_data['way2_title'] or not form_data['way2_text']:
            flash("All Two Ways to Apply section fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Two Ways to Apply Section', config, form_data)
        config.ways_eyebrow = form_data['ways_eyebrow']
        config.ways_heading = form_data['ways_heading']
        config.ways_text = form_data['ways_text']
        config.way1_title = form_data['way1_title']
        config.way1_text = form_data['way1_text']
        config.way2_title = form_data['way2_title']
        config.way2_text = form_data['way2_text']
        
    elif section == 'form_intro':
        form_data['form_eyebrow'] = request.form.get('form_eyebrow', '').strip()
        form_data['form_heading'] = request.form.get('form_heading', '').strip()
        form_data['form_text'] = request.form.get('form_text', '').strip()
        if not form_data['form_eyebrow'] or not form_data['form_heading'] or not form_data['form_text']:
            flash("All Online Application introduction fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Application Form Intro', config, form_data)
        config.form_eyebrow = form_data['form_eyebrow']
        config.form_heading = form_data['form_heading']
        config.form_text = form_data['form_text']
        
    elif section == 'contact':
        form_data['contact_label'] = request.form.get('contact_label', '').strip()
        form_data['contact_title'] = request.form.get('contact_title', '').strip()
        form_data['contact_phone'] = request.form.get('contact_phone', '').strip()
        form_data['contact_email'] = request.form.get('contact_email', '').strip()
        form_data['contact_address'] = request.form.get('contact_address', '').strip()
        form_data['contact_map_link'] = request.form.get('contact_map_link', '').strip()
        if not form_data['contact_label'] or not form_data['contact_title'] or not form_data['contact_phone'] or not form_data['contact_email'] or not form_data['contact_address'] or not form_data['contact_map_link']:
            flash("All Contact Strip fields are required.", "error")
            return redirect(url_for('admin_dashboard', tab='admission_content'))
            
        log_admission_content_change(session['admin_username'], 'Contact Strip Info', config, form_data)
        config.contact_label = form_data['contact_label']
        config.contact_title = form_data['contact_title']
        config.contact_phone = form_data['contact_phone']
        config.contact_email = form_data['contact_email']
        config.contact_address = form_data['contact_address']
        config.contact_map_link = form_data['contact_map_link']
        
    db.session.commit()
    flash(f"Admission page {section} section updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='admission_content'))

@app.route("/gallery")
def gallery_page():
    config = GalleryPageConfig.query.first()
    if not config:
        config = GalleryPageConfig()
        db.session.add(config)
        db.session.commit()
    photos = GalleryPhoto.query.all()
    videos = GalleryVideo.query.all()
    categories = GalleryCategory.query.order_by(GalleryCategory.id.asc()).all()
    return render_template(
        'gallery.html',
        name="Gallery",
        config=config,
        photos=photos,
        videos=videos,
        categories=categories
    )


@app.route("/admin/gallery/config", methods=['POST'])
def admin_gallery_config():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    config = GalleryPageConfig.query.first()
    if not config:
        config = GalleryPageConfig()
        db.session.add(config)
        
    form_data = {
        'hero_label': request.form.get('hero_label', '').strip(),
        'hero_title': request.form.get('hero_title', '').strip(),
        'hero_subtitle': request.form.get('hero_subtitle', '').strip(),
        'hero_bg_url': request.form.get('hero_bg_url', '').strip(),
        'stat1_num': request.form.get('stat1_num', '').strip(),
        'stat1_label': request.form.get('stat1_label', '').strip(),
        'stat2_num': request.form.get('stat2_num', '').strip(),
        'stat2_label': request.form.get('stat2_label', '').strip(),
        'stat3_num': request.form.get('stat3_num', '').strip(),
        'stat3_label': request.form.get('stat3_label', '').strip(),
        'photo_label': request.form.get('photo_label', '').strip(),
        'photo_title': request.form.get('photo_title', '').strip(),
        'photo_subtitle': request.form.get('photo_subtitle', '').strip(),
        'video_label': request.form.get('video_label', '').strip(),
        'video_title': request.form.get('video_title', '').strip(),
        'video_subtitle': request.form.get('video_subtitle', '').strip()
    }
    
    if not all(form_data.values()):
        flash("All configuration fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_config'))
        
    log_gallery_config_change(session['admin_username'], config, form_data)
    
    for key, val in form_data.items():
        setattr(config, key, val)
        
    db.session.commit()
    flash("Gallery settings updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_config'))


@app.route("/admin/gallery/photos/add", methods=['POST'])
def admin_gallery_photos_add():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    img_url = request.form.get('img_url', '').strip()
    category = request.form.get('category', '').strip()
    caption = request.form.get('caption', '').strip()
    
    # Check for file upload
    if 'photo_file' in request.files:
        file = request.files['photo_file']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                img_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='gallery_photos'))
                
    if not img_url or not category or not caption:
        flash("All photo fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_photos'))
        
    new_photo = GalleryPhoto(img_url=img_url, category=category, caption=caption)
    db.session.add(new_photo)
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Added Photo', caption)
    flash("Photo added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_photos'))


@app.route("/admin/gallery/photos/edit/<int:id>", methods=['POST'])
def admin_gallery_photos_edit(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    photo = GalleryPhoto.query.get_or_404(id)
    img_url = request.form.get('img_url', '').strip()
    category = request.form.get('category', '').strip()
    caption = request.form.get('caption', '').strip()
    
    # Check for file upload
    if 'photo_file' in request.files:
        file = request.files['photo_file']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                img_url = uploaded
            else:
                flash("Invalid image format.", "error")
                return redirect(url_for('admin_dashboard', tab='gallery_photos'))
                
    if not img_url or not category or not caption:
        flash("All photo fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_photos'))
        
    photo.img_url = img_url
    photo.category = category
    photo.caption = caption
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Edited Photo', caption)
    flash("Photo updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_photos'))


@app.route("/admin/gallery/photos/delete/<int:id>", methods=['POST'])
def admin_gallery_photos_delete(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    photo = GalleryPhoto.query.get_or_404(id)
    caption = photo.caption
    db.session.delete(photo)
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Deleted Photo', caption)
    flash("Photo deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_photos'))


@app.route("/admin/gallery/videos/add", methods=['POST'])
def admin_gallery_videos_add():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    yt_id = request.form.get('yt_id', '').strip()
    title = request.form.get('title', '').strip()
    duration = request.form.get('duration', '').strip()
    thumbnail_url = request.form.get('thumbnail_url', '').strip()
    
    # Check for file upload
    if 'thumbnail_file' in request.files:
        file = request.files['thumbnail_file']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                thumbnail_url = uploaded
            else:
                flash("Invalid thumbnail image format.", "error")
                return redirect(url_for('admin_dashboard', tab='gallery_videos'))
                
    # If thumbnail is empty, default to YouTube HQ thumbnail
    if not thumbnail_url and yt_id:
        thumbnail_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
        
    if not yt_id or not title or not duration or not thumbnail_url:
        flash("All video fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_videos'))
        
    new_video = GalleryVideo(yt_id=yt_id, title=title, duration=duration, thumbnail_url=thumbnail_url)
    db.session.add(new_video)
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Added Video', title)
    flash("Video added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_videos'))


@app.route("/admin/gallery/videos/edit/<int:id>", methods=['POST'])
def admin_gallery_videos_edit(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    video = GalleryVideo.query.get_or_404(id)
    yt_id = request.form.get('yt_id', '').strip()
    title = request.form.get('title', '').strip()
    duration = request.form.get('duration', '').strip()
    thumbnail_url = request.form.get('thumbnail_url', '').strip()
    
    # Check for file upload
    if 'thumbnail_file' in request.files:
        file = request.files['thumbnail_file']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                thumbnail_url = uploaded
            else:
                flash("Invalid thumbnail image format.", "error")
                return redirect(url_for('admin_dashboard', tab='gallery_videos'))
                
    # If thumbnail is empty, default to YouTube HQ thumbnail
    if not thumbnail_url and yt_id:
        thumbnail_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
        
    if not yt_id or not title or not duration or not thumbnail_url:
        flash("All video fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_videos'))
        
    video.yt_id = yt_id
    video.title = title
    video.duration = duration
    video.thumbnail_url = thumbnail_url
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Edited Video', title)
    flash("Video updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_videos'))


@app.route("/admin/gallery/videos/delete/<int:id>", methods=['POST'])
def admin_gallery_videos_delete(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    video = GalleryVideo.query.get_or_404(id)
    title = video.title
    db.session.delete(video)
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Deleted Video', title)
    flash("Video deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_videos'))


@app.route("/admin/gallery/categories/add", methods=['POST'])
def admin_gallery_categories_add():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    name = request.form.get('name', '').strip()
    if not name:
        flash("Category name is required.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_categories'))
        
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    if not slug:
        slug = "category-" + uuid.uuid4().hex[:6]
        
    # Check if category already exists
    existing = GalleryCategory.query.filter((GalleryCategory.name == name) | (GalleryCategory.slug == slug)).first()
    if existing:
        flash("A category with this name or slug already exists.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_categories'))
        
    new_cat = GalleryCategory(name=name, slug=slug)
    db.session.add(new_cat)
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Added Category', name)
    flash(f"Category '{name}' added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_categories'))


@app.route("/admin/gallery/categories/delete/<int:id>", methods=['POST'])
def admin_gallery_categories_delete(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    cat = GalleryCategory.query.get_or_404(id)
    
    # Check if there are photos associated with this category
    photo_count = GalleryPhoto.query.filter_by(category=cat.slug).count()
    if photo_count > 0:
        flash(f"Cannot delete category '{cat.name}' because it contains {photo_count} photo(s). Please delete or reassign the photos first.", "error")
        return redirect(url_for('admin_dashboard', tab='gallery_categories'))
        
    name = cat.name
    db.session.delete(cat)
    db.session.commit()
    
    log_gallery_media_change(session['admin_username'], 'Deleted Category', name)
    flash(f"Category '{name}' deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='gallery_categories'))

def process_uploaded_image(filepath, target_aspect_ratio=4/3):
    """
    Check if the image at filepath is portrait (height > width).
    If so, pad it with a dark navy background color to fit target_aspect_ratio (landscape).
    """
    import sys
    if '/usr/lib/python3/dist-packages' not in sys.path:
        sys.path.append('/usr/lib/python3/dist-packages')
    from PIL import Image, ImageOps
    
    try:
        with Image.open(filepath) as img:
            img = ImageOps.exif_transpose(img)
            w, h = img.size
            if h > w:
                new_w = int(h * target_aspect_ratio)
                background_color = (4, 20, 46) # Dark navy (#04142E)
                new_img = Image.new("RGB", (new_w, h), background_color)
                x_offset = (new_w - w) // 2
                new_img.paste(img, (x_offset, 0))
                new_img.save(filepath, format="JPEG" if img.format in ["JPEG", "MPO"] else img.format)
                return True
    except Exception as e:
        print("Error processing uploaded image:", e)
    return False


@app.route("/admin/academics/update", methods=['POST'])
def admin_academics_update():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    config = AcademicsPageConfig.query.first()
    if not config:
        config = AcademicsPageConfig()
        db.session.add(config)
        
    # Get form data for logging
    form_data = {
        'hero_label': request.form.get('hero_label', '').strip(),
        'hero_title': request.form.get('hero_title', '').strip(),
        'hero_subtitle': request.form.get('hero_subtitle', '').strip(),
        'overview_label': request.form.get('overview_label', '').strip(),
        'overview_title': request.form.get('overview_title', '').strip(),
        'overview_p1': request.form.get('overview_p1', '').strip(),
        'overview_p2': request.form.get('overview_p2', '').strip(),
        'methodology_label': request.form.get('methodology_label', '').strip(),
        'methodology_title': request.form.get('methodology_title', '').strip(),
        'methodology_description': request.form.get('methodology_description', '').strip(),
        'methodology_item1': request.form.get('methodology_item1', '').strip(),
        'methodology_item2': request.form.get('methodology_item2', '').strip(),
        'methodology_item3': request.form.get('methodology_item3', '').strip(),
        'methodology_item4': request.form.get('methodology_item4', '').strip(),
        'stat1_num': request.form.get('stat1_num', '').strip(),
        'stat1_label': request.form.get('stat1_label', '').strip(),
        'stat2_num': request.form.get('stat2_num', '').strip(),
        'stat2_label': request.form.get('stat2_label', '').strip(),
        'stat3_num': request.form.get('stat3_num', '').strip(),
        'stat3_label': request.form.get('stat3_label', '').strip(),
        'stat4_num': request.form.get('stat4_num', '').strip(),
        'stat4_label': request.form.get('stat4_label', '').strip(),
        'cta_label': request.form.get('cta_label', '').strip(),
        'cta_title': request.form.get('cta_title', '').strip(),
        'cta_text': request.form.get('cta_text', '').strip(),
        'cta_btn_text': request.form.get('cta_btn_text', '').strip(),
        'cta_btn_url': request.form.get('cta_btn_url', '').strip(),
    }
    log_academics_config_change(session['admin_username'], config, form_data)
    
    # Assign text fields
    config.hero_label = form_data['hero_label']
    config.hero_title = form_data['hero_title']
    config.hero_subtitle = form_data['hero_subtitle']
    
    config.overview_label = form_data['overview_label']
    config.overview_title = form_data['overview_title']
    config.overview_p1 = form_data['overview_p1']
    config.overview_p2 = form_data['overview_p2']
    
    config.methodology_label = form_data['methodology_label']
    config.methodology_title = form_data['methodology_title']
    config.methodology_description = form_data['methodology_description']
    config.methodology_item1 = form_data['methodology_item1']
    config.methodology_item2 = form_data['methodology_item2']
    config.methodology_item3 = form_data['methodology_item3']
    config.methodology_item4 = form_data['methodology_item4']
    
    config.stat1_num = form_data['stat1_num']
    config.stat1_label = form_data['stat1_label']
    config.stat2_num = form_data['stat2_num']
    config.stat2_label = form_data['stat2_label']
    config.stat3_num = form_data['stat3_num']
    config.stat3_label = form_data['stat3_label']
    config.stat4_num = form_data['stat4_num']
    config.stat4_label = form_data['stat4_label']
    
    config.cta_label = form_data['cta_label']
    config.cta_title = form_data['cta_title']
    config.cta_text = form_data['cta_text']
    config.cta_btn_text = form_data['cta_btn_text']
    config.cta_btn_url = form_data['cta_btn_url']
    
    # Handle overview image upload
    if 'overview_image' in request.files:
        file = request.files['overview_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                config.overview_img_url = uploaded
                # Perform orientation correction/padding
                full_path = os.path.join(app.root_path, 'static', 'images', uploaded)
                config.overview_img_is_portrait = process_uploaded_image(full_path)
                
    # Handle methodology image upload
    if 'methodology_image' in request.files:
        file = request.files['methodology_image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                config.methodology_img_url = uploaded
                # Perform orientation correction/padding
                full_path = os.path.join(app.root_path, 'static', 'images', uploaded)
                config.methodology_img_is_portrait = process_uploaded_image(full_path)
                
    db.session.commit()
    flash("Academics configuration updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='academics_config'))


@app.route("/admin/academics/curriculum/edit/<int:id>", methods=['POST'])
def admin_academics_curriculum_edit(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    card = AcademicsCurriculumCard.query.get_or_404(id)
    icon_svg = request.form.get('icon_svg', '').strip()
    title = request.form.get('title', '').strip()
    classes_range = request.form.get('classes_range', '').strip()
    description = request.form.get('description', '').strip()
    
    if not icon_svg or not title or not classes_range or not description:
        flash("All fields are required.", "error")
        return redirect(url_for('admin_dashboard', tab='academics_curriculum'))
        
    card.icon_svg = icon_svg
    card.title = title
    card.classes_range = classes_range
    card.description = description
    db.session.commit()
    
    log_academics_curriculum_change(session['admin_username'], 'Updated', card.title)
    flash("Curriculum card updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='academics_curriculum'))


def log_gallery_config_change(username, old_data, form_data):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Gallery Page Config Updated by {username})\n"
    log_entry += f"* **Administrator updated Gallery Page Config**:\n"
    
    has_changes = False
    for key, val in form_data.items():
        old_val = getattr(old_data, key, '')
        if old_val != val:
            log_entry += f"  * **{key.replace('_', ' ').title()}**: \"{old_val}\" &rarr; \"{val}\"\n"
            has_changes = True
            
    if not has_changes:
        log_entry += f"  * No visible content changes made.\n"
        
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


def log_gallery_media_change(username, action, item_name):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Gallery Media Updated by {username})\n"
    log_entry += f"* **Administrator performed: {action} on \"{item_name}\"**\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


@app.route("/admin/academics/topper/add", methods=['POST'])
def admin_academics_topper_add():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    title = request.form.get('title', '').strip()
    class_name = request.form.get('class_name', '').strip()
    year = request.form.get('year', '').strip()
    description = request.form.get('description', '').strip()
    
    image_url = "topper.jpg"
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
                
    if not title or not class_name or not year:
        flash("Title, Class, and Year are required fields.", "error")
        return redirect(url_for('admin_dashboard', tab='academics_toppers'))
        
    new_topper = AcademicTopper(
        title=title,
        class_name=class_name,
        year=year,
        image_url=image_url,
        description=description
    )
    db.session.add(new_topper)
    db.session.commit()
    
    log_academics_topper_change(session['admin_username'], 'Added', title)
    flash("Topper banner added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='academics_toppers'))


@app.route("/admin/academics/topper/edit/<int:id>", methods=['POST'])
def admin_academics_topper_edit(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    topper = AcademicTopper.query.get_or_404(id)
    title = request.form.get('title', '').strip()
    class_name = request.form.get('class_name', '').strip()
    year = request.form.get('year', '').strip()
    description = request.form.get('description', '').strip()
    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                topper.image_url = uploaded
                
    if not title or not class_name or not year:
        flash("Title, Class, and Year are required fields.", "error")
        return redirect(url_for('admin_dashboard', tab='academics_toppers'))
        
    topper.title = title
    topper.class_name = class_name
    topper.year = year
    topper.description = description
    db.session.commit()
    
    log_academics_topper_change(session['admin_username'], 'Updated', title)
    flash("Topper banner updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='academics_toppers'))


@app.route("/admin/academics/topper/delete/<int:id>", methods=['POST'])
def admin_academics_topper_delete(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    topper = AcademicTopper.query.get_or_404(id)
    title = topper.title
    db.session.delete(topper)
    db.session.commit()
    
    log_academics_topper_change(session['admin_username'], 'Deleted', title)
    flash("Topper banner deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='academics_toppers'))


def log_birthday_change(username, action, name):
    log_file_path = os.path.join(app.root_path, 'project_knowledge.md')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n## Admin Update: {timestamp} (Birthdays {action} by {username})\n"
    log_entry += f"* **Administrator {action.lower()} birthday record for: \"{name}\"**\n"
    
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to project_knowledge.md: {e}")


@app.route("/admin/birthday/add", methods=['POST'])
def admin_birthday_add():
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    name = request.form.get('name', '').strip()
    birthday = request.form.get('birthday', '').strip()
    role = request.form.get('role', '').strip()
    class_name = request.form.get('class_name', '').strip()
    
    image_url = "logo.png"
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                image_url = uploaded
                
    if not name or not birthday or not role:
        flash("Name, Birthday, and Role are required fields.", "error")
        return redirect(url_for('admin_dashboard', tab='birthdays'))
        
    new_birthday = BirthdayRecord(
        name=name,
        birthday=birthday,
        role=role,
        class_name=class_name,
        image_url=image_url
    )
    db.session.add(new_birthday)
    db.session.commit()
    
    log_birthday_change(session['admin_username'], 'Added', name)
    flash("Birthday record added successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='birthdays'))


@app.route("/admin/birthday/edit/<int:id>", methods=['POST'])
def admin_birthday_edit(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    record = BirthdayRecord.query.get_or_404(id)
    name = request.form.get('name', '').strip()
    birthday = request.form.get('birthday', '').strip()
    role = request.form.get('role', '').strip()
    class_name = request.form.get('class_name', '').strip()
    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            uploaded = save_uploaded_file(file)
            if uploaded:
                record.image_url = uploaded
                
    if not name or not birthday or not role:
        flash("Name, Birthday, and Role are required fields.", "error")
        return redirect(url_for('admin_dashboard', tab='birthdays'))
        
    record.name = name
    record.birthday = birthday
    record.role = role
    record.class_name = class_name
    db.session.commit()
    
    log_birthday_change(session['admin_username'], 'Updated', name)
    flash("Birthday record updated successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='birthdays'))


@app.route("/admin/birthday/delete/<int:id>", methods=['POST'])
def admin_birthday_delete(id):
    if not session.get('admin_logged_in'):
        flash("Please log in to access the admin dashboard.", "error")
        return redirect(url_for('admin_login'))
        
    record = BirthdayRecord.query.get_or_404(id)
    name = record.name
    db.session.delete(record)
    db.session.commit()
    
    log_birthday_change(session['admin_username'], 'Deleted', name)
    flash("Birthday record deleted successfully!", "success")
    return redirect(url_for('admin_dashboard', tab='birthdays'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
else:
    print("ran with flask run")
