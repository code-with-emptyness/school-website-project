from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HeroSection(db.Model):
    __tablename__ = 'hero_section'
    
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(200), nullable=False)
    subheading = db.Column(db.String(200), nullable=False)
    button_text = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class PrincipalCard(db.Model):
    __tablename__ = 'principal_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(50), unique=True, nullable=False) # 'card1' or 'card2'
    title = db.Column(db.String(100), nullable=False) # e.g. 'FROM THE DESK OF'
    subtitle = db.Column(db.String(100), nullable=False) # e.g. 'Principal'
    image_url = db.Column(db.String(200), nullable=False, default='principal.jpg')
    message_heading = db.Column(db.String(200), nullable=False) # e.g. 'Message from Principal'
    message_p1 = db.Column(db.Text, nullable=False)
    message_p2 = db.Column(db.Text, nullable=False)
    signature_name = db.Column(db.String(100), nullable=False) # e.g. 'Dr. XYZ'
    signature_role = db.Column(db.String(100), nullable=False) # e.g. 'Principal'

class Facility(db.Model):
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(50), nullable=False) # emoji or class name
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200), nullable=False, default='#')

class VisionContent(db.Model):
    __tablename__ = 'vision_content'
    
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False, default='OUR VISION')
    heading = db.Column(db.String(200), nullable=False)
    p1 = db.Column(db.Text, nullable=False)
    p2 = db.Column(db.Text, nullable=False)
    p3 = db.Column(db.Text, nullable=False)

class ValueCard(db.Model):
    __tablename__ = 'value_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=True) 
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False, default='integrity.jpg')

class AboutPageConfig(db.Model):
    __tablename__ = 'about_page_config'
    
    id = db.Column(db.Integer, primary_key=True)
    # Hero Section
    hero_eyebrow = db.Column(db.String(200), nullable=False)
    hero_heading = db.Column(db.String(200), nullable=False)
    hero_description = db.Column(db.Text, nullable=False)
    
    # Who We Are Section
    who_eyebrow = db.Column(db.String(200), nullable=False)
    who_heading = db.Column(db.String(200), nullable=False)
    who_p1 = db.Column(db.Text, nullable=False)
    who_p2 = db.Column(db.Text, nullable=False)
    who_image_url = db.Column(db.String(200), nullable=False, default='placeholder.jpg')
    
    # History Section
    history_eyebrow = db.Column(db.String(200), nullable=False)
    history_heading = db.Column(db.String(200), nullable=False)
    history_p1 = db.Column(db.Text, nullable=False)
    history_p2 = db.Column(db.Text, nullable=False)
    history_image_url = db.Column(db.String(200), nullable=False, default='placeholder.jpg')
    
    # Vision & Mission
    vm_eyebrow = db.Column(db.String(200), nullable=False)
    vm_heading = db.Column(db.String(200), nullable=False)
    vm_vision_title = db.Column(db.String(200), nullable=False)
    vm_vision_desc = db.Column(db.Text, nullable=False)
    vm_mission_title = db.Column(db.String(200), nullable=False)
    vm_mission_bullets = db.Column(db.Text, nullable=False) # Newline separated list
    
    # Management Section
    mgmt_eyebrow = db.Column(db.String(200), nullable=False)
    mgmt_heading = db.Column(db.String(200), nullable=False)
    mgmt_p1 = db.Column(db.Text, nullable=False)
    mgmt_p2 = db.Column(db.Text, nullable=False)
    mgmt_image_url = db.Column(db.String(200), nullable=False, default='placeholder.jpg')
    
    # Principal Message Section
    principal_eyebrow = db.Column(db.String(200), nullable=False)
    principal_heading = db.Column(db.String(200), nullable=False)
    principal_p1 = db.Column(db.Text, nullable=False)
    principal_p2 = db.Column(db.Text, nullable=False)
    principal_p3 = db.Column(db.Text, nullable=False)
    principal_signature_name = db.Column(db.String(100), nullable=False)
    principal_signature_role = db.Column(db.String(100), nullable=False)
    principal_image_url = db.Column(db.String(200), nullable=False, default='placeholder.jpg')
    
    # Achievements Section Banner Image
    achievements_banner_url = db.Column(db.String(200), nullable=False, default='placeholder.jpg')

class AboutPageValue(db.Model):
    __tablename__ = 'about_page_values'
    
    id = db.Column(db.Integer, primary_key=True)
    icon_svg = db.Column(db.Text, nullable=False) # SVG element code or emoji
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class AboutPageAchievement(db.Model):
    __tablename__ = 'about_page_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

class Notice(db.Model):
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    target = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    issued_by = db.Column(db.String(100), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image1_url = db.Column(db.String(200), nullable=False)
    image2_url = db.Column(db.String(200), nullable=False)
    video_url = db.Column(db.String(200), nullable=False)
    video_thumb_url = db.Column(db.String(200), nullable=False)
    tags = db.Column(db.String(200), nullable=False)

class AcademicCalendar(db.Model):
    __tablename__ = 'academic_calendar'
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False, default='Annual_planner.png')
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class ContactQuery(db.Model):
    __tablename__ = 'contact_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class AdmissionSetting(db.Model):
    __tablename__ = 'admission_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    admissions_open = db.Column(db.Boolean, default=True, nullable=False)
    closed_message_heading = db.Column(db.String(200), nullable=False, default="Admissions Closed")
    closed_message_body = db.Column(db.Text, nullable=False, default="Thank you for your interest. Admissions for the current academic session are now closed. Please check back later.")


class SubjectItem(db.Model):
    __tablename__ = 'subject_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    svg_icon = db.Column(db.Text, nullable=False)


class DocItem(db.Model):
    __tablename__ = 'doc_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(200), nullable=False)
    svg_icon = db.Column(db.Text, nullable=False)


class AdmissionQuery(db.Model):
    __tablename__ = 'admission_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    class_applying = db.Column(db.String(50), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    prev_school = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class AdmissionPageConfig(db.Model):
    __tablename__ = 'admission_page_config'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Hero Section
    hero_eyebrow = db.Column(db.String(200), nullable=False, default="Admissions 2025–26")
    hero_heading = db.Column(db.String(200), nullable=False, default="Begin Your Journey at Greenfield Academy")
    hero_subheading = db.Column(db.Text, nullable=False, default="Join a learning environment that nurtures academic excellence, discipline, and character. Admissions are now open for the upcoming academic year.")
    
    # Overview Section
    overview_eyebrow = db.Column(db.String(200), nullable=False, default="Admission Overview")
    overview_heading = db.Column(db.String(200), nullable=False, default="How Admissions Work")
    overview_p1 = db.Column(db.Text, nullable=False, default="Students seeking admission are required to complete the admission process and fulfil all eligibility requirements prescribed by the school.")
    overview_p2 = db.Column(db.Text, nullable=False, default="Admission is granted strictly on the basis of the candidate's performance in the admission test and is not influenced by marks or grades obtained at any prior institution.")
    
    # Office Visit Section
    visit_title = db.Column(db.String(200), nullable=False, default="Visit Us in Person")
    visit_text = db.Column(db.Text, nullable=False, default="Parents and guardians are welcome to visit the school office directly for admission, information, or any related queries during office hours.")
    office_days = db.Column(db.String(100), nullable=False, default="Monday – Saturday")
    office_hours = db.Column(db.String(100), nullable=False, default="09:00 AM – 02:00 PM")
    office_note = db.Column(db.String(200), nullable=False, default="Office remains closed on Sundays and public holidays.")
    
    # Process Section
    process_eyebrow = db.Column(db.String(200), nullable=False, default="Admission Process")
    process_heading = db.Column(db.String(200), nullable=False, default="Six Steps to Enrollment")
    process_text = db.Column(db.Text, nullable=False, default="Our admission process is designed to be straightforward and transparent. Here is what you can expect from the moment you apply to the day your child joins us.")
    
    # Test expectations Section
    test_heading = db.Column(db.String(200), nullable=False, default="What to Expect")
    test_p1 = db.Column(db.Text, nullable=False, default="All students applying for admission are required to appear for an admission test comprising a written examination conducted at the school premises.")
    test_p2 = db.Column(db.Text, nullable=False, default="No specific syllabus is prescribed for the admission test. Candidates should possess a sound knowledge of subjects appropriate for the class lower than the one for which admission is sought.")
    test_p3 = db.Column(db.Text, nullable=False, default="Admission is granted strictly on the basis of the candidate's performance in the admission test and not on marks obtained elsewhere.")
    test_note = db.Column(db.Text, nullable=False, default="Please Note: The admission test cannot be rescheduled except under exceptional circumstances at the sole discretion of the school administration.")
    
    # Process Steps Details
    step1_title = db.Column(db.String(200), nullable=False, default="Submit the Online Admission Form")
    step1_text = db.Column(db.Text, nullable=False, default="Complete and submit the admission form through our online portal or collect a physical copy from the school office. Ensure all details are accurate before submission.")
    
    step2_title = db.Column(db.String(200), nullable=False, default="Admission Team Contact")
    step2_text = db.Column(db.Text, nullable=False, default="Once your application is received, a member of our admissions team will review the details and contact you to confirm the next steps and the date for the admission test.")
    
    step3_title = db.Column(db.String(200), nullable=False, default="Appear for the Admission Test")
    step3_text = db.Column(db.Text, nullable=False, default="The candidate must appear in person for a written admission test conducted at the school premises on the designated date and time communicated by the admissions team.")
    
    step4_title = db.Column(db.String(200), nullable=False, default="Admission Test Evaluation")
    step4_text = db.Column(db.Text, nullable=False, default="The written examination is evaluated by the school's academic panel. Results are assessed on the basis of the candidate's knowledge and aptitude for the class applied for.")
    
    step5_title = db.Column(db.String(200), nullable=False, default="Submission of Required Documents")
    step5_text = db.Column(db.Text, nullable=False, default="Candidates who qualify the admission test are required to submit all mandatory documents to the school office within the timeframe specified by the admissions team.")
    
    step6_title = db.Column(db.String(200), nullable=False, default="Confirmation of Admission")
    step6_text = db.Column(db.Text, nullable=False, default="Upon verification of documents and completion of the admission fee, the admission is formally confirmed and a welcome letter is issued to the student and family.")

    # Documents Section Content
    doc_eyebrow = db.Column(db.String(200), nullable=False, default="Required Documents")
    doc_heading = db.Column(db.String(200), nullable=False, default="Documents to Submit")
    doc_text = db.Column(db.Text, nullable=False, default="The following documents must be submitted to the school office after the candidate has qualified the admission test and before admission can be confirmed.")
    tc_notice_heading = db.Column(db.String(200), nullable=False, default="Transfer Certificate Notice:")
    tc_notice_text = db.Column(db.Text, nullable=False, default="Admission can be finalised only after submission of a valid Transfer Certificate (T.C.). Transfer Certificates issued by schools outside Uttar Pradesh must be countersigned by the education authorities of the respective state before submission.")

    # Two Ways Section
    ways_eyebrow = db.Column(db.String(200), nullable=False, default="How to Apply")
    ways_heading = db.Column(db.String(200), nullable=False, default="Two Ways to Begin")
    ways_text = db.Column(db.Text, nullable=False, default="You may apply for admission through our online form or visit the school office directly — whichever is most convenient for your family. Our team will guide you through every step.")
    way1_title = db.Column(db.String(200), nullable=False, default="Apply Online")
    way1_text = db.Column(db.Text, nullable=False, default="Fill out the admission form below. Once submitted, our admissions team will review your application and reach out to you with the next steps and required guidance.")
    way2_title = db.Column(db.String(200), nullable=False, default="Visit the School Office")
    way2_text = db.Column(db.Text, nullable=False, default="Parents and guardians are welcome to visit the school office directly during office hours for admission inquiries, assistance, or to collect a physical form.")

    # Form Section Intro
    form_eyebrow = db.Column(db.String(200), nullable=False, default="Online Application")
    form_heading = db.Column(db.String(200), nullable=False, default="Submit Your Application")
    form_text = db.Column(db.Text, nullable=False, default="Complete the form below to begin the admission process. Our team will contact you within 2 working days to confirm your application and provide further guidance.")

    # Contact Strip Section
    contact_label = db.Column(db.String(200), nullable=False, default="Get in Touch")
    contact_title = db.Column(db.String(200), nullable=False, default="Admissions Office")
    contact_phone = db.Column(db.String(100), nullable=False, default="+91 12345 67890")
    contact_email = db.Column(db.String(200), nullable=False, default="admissions@greenfieldacademy.edu.in")
    contact_address = db.Column(db.String(300), nullable=False, default="123 Academy Road, Lucknow, U.P.")
    contact_map_link = db.Column(db.String(300), nullable=False, default="#")

class ContactPageConfig(db.Model):
    __tablename__ = 'contact_page_config'
    
    id = db.Column(db.Integer, primary_key=True)
    # Address Info
    address_line1 = db.Column(db.String(200), nullable=False, default="G.T. Road, Reraiya, Near Dak Bunglow")
    address_line2 = db.Column(db.String(200), nullable=False, default="Fatehpur, Uttar Pradesh - 212601")
    # Phone Info
    phone1 = db.Column(db.String(100), nullable=False, default="+91 70801 23456")
    phone2 = db.Column(db.String(100), nullable=False, default="+91 5180 223456")
    # Email Info
    email1 = db.Column(db.String(200), nullable=False, default="info@stxaviersfatehpur.org")
    email2 = db.Column(db.String(200), nullable=False, default="admissions@stxaviersfatehpur.org")
    # WhatsApp Info
    whatsapp = db.Column(db.String(100), nullable=False, default="+91 70801 23456")
    # Office Timings
    office_hours_mon_fri = db.Column(db.String(100), nullable=False, default="8:00 AM – 4:00 PM")
    office_hours_sat = db.Column(db.String(100), nullable=False, default="8:00 AM – 1:00 PM")
    office_hours_sun = db.Column(db.String(100), nullable=False, default="Closed")
    # School Timings
    school_hours_primary = db.Column(db.String(100), nullable=False, default="8:00 AM – 1:30 PM")
    school_hours_middle = db.Column(db.String(100), nullable=False, default="8:00 AM – 2:30 PM")
    school_hours_senior = db.Column(db.String(100), nullable=False, default="8:00 AM – 3:00 PM")
    # Admission Office Timings
    admission_hours_mon_sat = db.Column(db.String(100), nullable=False, default="9:00 AM – 3:00 PM")
    admission_hours_sun = db.Column(db.String(100), nullable=False, default="Closed")
    admission_hours_note = db.Column(db.String(200), nullable=False, default="* Timings may vary during exams and holidays")
    # Maps Info
    map_iframe_src = db.Column(db.Text, nullable=False, default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3596.223871780447!2d80.81422797523956!3d25.666993177402636!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x399d8d002a2012d9%3A0x6d05f3241b714b2e!2sSt.%20Xavier&#39;s%20High%20School!5e0!3m2!1sen!2sin!4v1718870000000!5m2!1sen!2sin")
    map_directions_url = db.Column(db.String(300), nullable=False, default="https://maps.google.com/?q=St.+Xavier's+High+School+Fatehpur+Uttar+Pradesh")

class FAQItem(db.Model):
    __tablename__ = 'faq_items'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.Text, nullable=False)

class GalleryPageConfig(db.Model):
    __tablename__ = 'gallery_page_config'
    
    id = db.Column(db.Integer, primary_key=True)
    # Hero Section
    hero_label = db.Column(db.String(200), nullable=False, default="Greenfield Academy")
    hero_title = db.Column(db.String(200), nullable=False, default="Our Story in Every Frame")
    hero_subtitle = db.Column(db.String(500), nullable=False, default="A visual journey through our campus, achievements, and vibrant student life — capturing the spirit of excellence that defines our community.")
    hero_bg_url = db.Column(db.String(500), nullable=False, default="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1600&auto=format&fit=crop&q=80")
    
    # Stats
    stat1_num = db.Column(db.String(50), nullable=False, default="500+")
    stat1_label = db.Column(db.String(100), nullable=False, default="Memories Captured")
    stat2_num = db.Column(db.String(50), nullable=False, default="12")
    stat2_label = db.Column(db.String(100), nullable=False, default="Years of Legacy")
    stat3_num = db.Column(db.String(50), nullable=False, default="48")
    stat3_label = db.Column(db.String(100), nullable=False, default="Events Documented")
    
    # Photo Section Headers
    photo_label = db.Column(db.String(200), nullable=False, default="Visual Archive")
    photo_title = db.Column(db.String(200), nullable=False, default="Campus & Student Life")
    photo_subtitle = db.Column(db.String(500), nullable=False, default="Browse through our collection of photographs celebrating every facet of life at Greenfield Academy.")
    
    # Video Section Headers
    video_label = db.Column(db.String(200), nullable=False, default="Film Archive")
    video_title = db.Column(db.String(200), nullable=False, default="Watch Our Story Unfold")
    video_subtitle = db.Column(db.String(500), nullable=False, default="From milestone events to everyday moments of learning and growth — experience Greenfield Academy through motion.")

class GalleryPhoto(db.Model):
    __tablename__ = 'gallery_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=False) # campus, classroom, sports, cultural
    caption = db.Column(db.String(300), nullable=False)

class GalleryVideo(db.Model):
    __tablename__ = 'gallery_videos'
    
    id = db.Column(db.Integer, primary_key=True)
    yt_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=False)

class GalleryCategory(db.Model):
    __tablename__ = 'gallery_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)

class AcademicsPageConfig(db.Model):
    __tablename__ = 'academics_page_config'
    
    id = db.Column(db.Integer, primary_key=True)
    # Hero Section
    hero_label = db.Column(db.String(200), nullable=False, default="Academics")
    hero_title = db.Column(db.String(300), nullable=False, default="Academic Excellence Rooted in Knowledge, Values, and Innovation")
    hero_subtitle = db.Column(db.Text, nullable=False, default="At St. Xavier's High School, Fatehpur, academics form the foundation of our commitment to nurturing confident, responsible, and future-ready learners. Affiliated with CBSE and offering education from Class I to XII, we provide a balanced academic environment.")
    
    # Overview Section
    overview_label = db.Column(db.String(200), nullable=False, default="Overview")
    overview_title = db.Column(db.String(300), nullable=False, default="A Comprehensive Educational Journey")
    overview_p1 = db.Column(db.Text, nullable=False, default="St. Xavier's High School follows the CBSE curriculum and offers a comprehensive educational journey from primary to senior secondary levels.")
    overview_p2 = db.Column(db.Text, nullable=False, default="Through a blend of classroom instruction, practical experiences, and technology-enabled learning, students are encouraged to explore, question, and excel. We strive to create an atmosphere where every learner is supported, challenged, and inspired to achieve their highest potential.")
    overview_img_url = db.Column(db.String(500), nullable=False, default="class1.jpg")
    overview_img_is_portrait = db.Column(db.Boolean, nullable=False, default=False)
    
    # Methodology Section
    methodology_label = db.Column(db.String(200), nullable=False, default="Methodology")
    methodology_title = db.Column(db.String(300), nullable=False, default="Beyond Traditional Textbooks")
    methodology_description = db.Column(db.Text, nullable=False, default="Our teaching approach combines modern educational practices with strong academic discipline, ensuring students acquire knowledge while developing confidence and creativity.")
    methodology_item1 = db.Column(db.String(300), nullable=False, default="Smart Classroom Integration & Interactive Sessions")
    methodology_item2 = db.Column(db.String(300), nullable=False, default="Concept-Oriented & Activity-Based Learning")
    methodology_item3 = db.Column(db.String(300), nullable=False, default="Personalized Remedial Support & Teacher Mentorship")
    methodology_item4 = db.Column(db.String(300), nullable=False, default="Technology-Assisted Teaching Methods")
    methodology_img_url = db.Column(db.String(500), nullable=False, default="class.jpg")
    methodology_img_is_portrait = db.Column(db.Boolean, nullable=False, default=False)
    
    # At a Glance
    stat1_num = db.Column(db.String(50), nullable=False, default="1500+")
    stat1_label = db.Column(db.String(200), nullable=False, default="Enrolled Students")
    stat2_num = db.Column(db.String(50), nullable=False, default="100+")
    stat2_label = db.Column(db.String(200), nullable=False, default="Faculty Members")
    stat3_num = db.Column(db.String(50), nullable=False, default="99%")
    stat3_label = db.Column(db.String(200), nullable=False, default="Board Success Rate")
    stat4_num = db.Column(db.String(50), nullable=False, default="20:1")
    stat4_label = db.Column(db.String(200), nullable=False, default="Student-Teacher Ratio")
    
    # Footer CTA
    cta_label = db.Column(db.String(200), nullable=False, default="Looking Forward")
    cta_title = db.Column(db.String(300), nullable=False, default="Shaping Future Leaders")
    cta_text = db.Column(db.Text, nullable=False, default="At St. Xavier's High School, Fatehpur, we believe that education is not merely the acquisition of knowledge but the development of character, confidence, and capability. Through academic excellence, innovative teaching practices, and a nurturing environment, we prepare students to become responsible citizens and successful leaders of tomorrow.")
    cta_btn_text = db.Column(db.String(200), nullable=False, default="Explore Admissions")
    cta_btn_url = db.Column(db.String(300), nullable=False, default="#")

class AcademicsCurriculumCard(db.Model):
    __tablename__ = 'academics_curriculum_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    icon_svg = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    classes_range = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

class AcademicTopper(db.Model):
    __tablename__ = 'academic_toppers'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) # e.g. "Class X Board Toppers"
    class_name = db.Column(db.String(100), nullable=False) # e.g. "Class X" or "Class XI"
    year = db.Column(db.String(100), nullable=False) # e.g. "2024-2025"
    image_url = db.Column(db.String(500), nullable=False, default="topper.jpg") # e.g. "topper.jpg" or "topper2.jpg"
    description = db.Column(db.Text, nullable=True)

class BirthdayRecord(db.Model):
    __tablename__ = 'birthday_records'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.String(100), nullable=False) # e.g. "28th June"
    role = db.Column(db.String(100), nullable=False) # "Teacher" or "Student"
    class_name = db.Column(db.String(100), nullable=True) # e.g. "Class X-A"
    image_url = db.Column(db.String(500), nullable=False, default="logo.png")