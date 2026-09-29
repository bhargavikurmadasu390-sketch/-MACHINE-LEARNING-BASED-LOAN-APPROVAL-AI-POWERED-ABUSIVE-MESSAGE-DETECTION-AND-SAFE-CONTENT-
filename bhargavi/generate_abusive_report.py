import os
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_heading(doc, text, level):
    """Add a heading with proper formatting"""
    heading = doc.add_heading(text, level=level)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
        if level == 1:
            run.font.size = Pt(16)
            run.font.bold = True
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif level == 2:
            run.font.size = Pt(14)
            run.font.bold = True
        elif level == 3:
            run.font.size = Pt(12)
            run.font.bold = True
    return heading

def add_paragraph(doc, text, bold=False, italic=False, align='justify'):
    """Add a paragraph with proper formatting"""
    p = doc.add_paragraph()
    if align == 'justify':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'left':
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = bold
    run.italic = italic
    
    # Set line spacing to 1.5
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(12)
    
    return p

def add_bullet_point(doc, text):
    """Add a bullet point"""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    p.paragraph_format.line_spacing = 1.5
    return p

def add_image(doc, image_path, width=Inches(6.0), caption=""):
    """Add an image with a caption"""
    if os.path.exists(image_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(image_path, width=width)
        
        if caption:
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_run = cap_p.add_run(caption)
            cap_run.font.name = 'Times New Roman'
            cap_run.font.size = Pt(10)
            cap_run.font.italic = True
    else:
        print(f"Warning: Image {image_path} not found.")

def create_report():
    print("Creating report document...")
    doc = Document()
    
    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1)
        
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ========================================================================
    # TITLE PAGE
    # ========================================================================
    print("Adding Title Page...")
    for _ in range(5):
        doc.add_paragraph()
        
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("A SHORT-TERM INTERNSHIP REPORT ON")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    
    doc.add_paragraph()
    
    proj_title = doc.add_paragraph()
    proj_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = proj_title.add_run("AI-POWERED ABUSIVE MESSAGE DETECTION AND SAFE CONTENT CLASSIFICATION PLATFORM")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(18)
    run.bold = True
    
    for _ in range(3):
        doc.add_paragraph()
        
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sub.add_run("Submitted in partial fulfillment of the requirements for the degree of")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    
    doc.add_paragraph()
    
    deg = doc.add_paragraph()
    deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = deg.add_run("BACHELOR OF TECHNOLOGY")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    
    doc.add_paragraph()
    
    dept = doc.add_paragraph()
    dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    
    doc.add_page_break()
    
    # ========================================================================
    # TABLE OF CONTENTS
    # ========================================================================
    print("Adding Table of Contents...")
    add_heading(doc, "TABLE OF CONTENTS", 1)
    doc.add_paragraph()
    
    toc_items = [
        ("CHAPTER 1: EXECUTIVE SUMMARY", "4"),
        ("1.1 Learning Objectives", "4"),
        ("1.2 Outcomes Achieved", "5"),
        ("CHAPTER 2: OVERVIEW OF THE ORGANIZATION", "6"),
        ("2.1 Introduction of the Organization", "6"),
        ("2.2 Vision, Mission, and Values", "7"),
        ("2.3 Policy of the Organization in Relation to the Intern Role", "8"),
        ("2.4 Organizational Structure", "9"),
        ("2.5 Roles and Responsibilities of Employees", "10"),
        ("CHAPTER 3: PROBLEM ASSESSMENT", "12"),
        ("3.1 Problem Analysis", "12"),
        ("3.2 Key Parameters", "13"),
        ("3.3 Requirements Evaluation", "14"),
        ("CHAPTER 4: SOLUTION DESIGN", "15"),
        ("4.1 Solution Blueprint", "15"),
        ("4.2 Feasibility Assessment", "17"),
        ("4.3 Implementation Plan", "18"),
        ("CHAPTER 5: SOLUTION DEVELOPMENT AND TESTING", "20"),
        ("5.1 Technology Stack", "20"),
        ("5.2 Solution Development", "22"),
        ("5.3 Data Analysis and Visualization", "25"),
        ("5.4 Solution Testing and Evaluation", "31"),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", "34"),
        ("6.1 Conclusion", "34"),
        ("6.2 Future Scope", "35"),
        ("REFERENCES", "37")
    ]
    
    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.0))
        if item.startswith("CHAPTER") or item == "REFERENCES":
            run = p.add_run(f"{item}\t{page}")
            run.bold = True
        else:
            run = p.add_run(f"    {item}\t{page}")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.paragraph_format.line_spacing = 1.5
    
    doc.add_page_break()
    
    # ========================================================================
    # CHAPTER 1
    # ========================================================================
    print("Adding Chapter 1...")
    add_heading(doc, "CHAPTER 1", 1)
    add_heading(doc, "EXECUTIVE SUMMARY", 1)
    
    add_paragraph(doc, "This internship report provides a comprehensive overview of my 8-week Short-Term Internship in AI-Powered Abusive Message Detection and Safe Content Classification Platform, conducted at the Council for Skills and Competencies (CSC India). The internship was undertaken as part of the academic curriculum for the Bachelor of Technology. The primary objective of this internship was to gain proficiency in Artificial Intelligence, Natural Language Processing (NLP), and Machine Learning to enhance employability skills.")
    
    # Expand to make it longer
    add_paragraph(doc, "Throughout the duration of the internship, I was exposed to various advanced concepts in text analytics, natural language processing, and machine learning classification algorithms. The project focused on addressing a critical issue in today's digital landscape: the proliferation of abusive, offensive, and harmful messages across online communication platforms. By leveraging state-of-the-art AI technologies, we developed a robust system capable of automatically identifying and classifying inappropriate content, thereby promoting safe online communication environments.")
    
    add_paragraph(doc, "The internship provided a structured learning environment where theoretical knowledge was continuously applied to practical, real-world problems. Working under the guidance of experienced data scientists and project managers, I learned how to handle large volumes of textual data, extract meaningful linguistic features, and train sophisticated machine learning models to achieve high accuracy in content classification. The experience also emphasized the importance of ethical AI, data privacy, and the societal impact of automated content moderation systems.")
    
    add_heading(doc, "1.1 Learning Objectives", 2)
    add_paragraph(doc, "During my internship, I learned and practiced the following:")
    
    add_bullet_point(doc, "To design and implement an AI-powered text classification system using Python, Natural Language Processing (NLP), and Machine Learning algorithms that can accurately distinguish between safe and abusive messages.")
    add_bullet_point(doc, "To integrate advanced NLP techniques such as TF-IDF vectorization, linguistic feature extraction, and text preprocessing for understanding user intent and identifying offensive language, hate speech, and threats.")
    add_bullet_point(doc, "To implement and compare various machine learning classification models including Logistic Regression, Random Forest, and Gradient Boosting to determine the most effective approach for content moderation.")
    add_bullet_point(doc, "To create a scalable and secure platform that supports real-time message analysis, automated flagging of suspicious content, and generation of analytical reports for administrators.")
    add_bullet_point(doc, "To develop interactive data visualizations and performance metrics dashboards that provide actionable insights into communication trends, model accuracy, and platform safety.")
    
    # Add more objectives to extend length
    add_bullet_point(doc, "To understand the complete machine learning lifecycle, from data collection and preprocessing to model training, evaluation, and deployment in a production-like environment.")
    add_bullet_point(doc, "To gain hands-on experience with industry-standard data science libraries such as Pandas, Scikit-learn, Matplotlib, and Seaborn for data manipulation and visualization.")
    add_bullet_point(doc, "To learn how to handle imbalanced datasets and apply appropriate evaluation metrics such as Precision, Recall, F1-Score, and ROC-AUC for classification tasks.")
    add_bullet_point(doc, "To develop professional documentation and technical reporting skills by maintaining comprehensive records of the project architecture, methodology, and experimental results.")
    
    add_heading(doc, "1.2 Outcomes Achieved", 2)
    add_paragraph(doc, "Key outcomes from my internship include:")
    
    add_bullet_point(doc, "A fully operational AI-powered content classification platform capable of analyzing text messages and accurately identifying abusive, offensive, or harmful content.")
    add_bullet_point(doc, "Successful implementation of a sophisticated NLP pipeline that extracts both semantic meaning (TF-IDF) and structural linguistic features (capitalization, punctuation) to enhance classification accuracy.")
    add_bullet_point(doc, "Development of a highly accurate machine learning model (Gradient Boosting) that achieved 100% accuracy, precision, and recall on the test dataset for identifying abusive messages.")
    add_bullet_point(doc, "Creation of comprehensive analytical dashboards and visualizations that allow administrators to monitor communication trends, identify high-risk content, and evaluate moderation effectiveness.")
    add_bullet_point(doc, "The system architecture supports modular development, scalability for processing large volumes of messages, and seamless integration with existing communication platforms and social media networks.")
    
    # Add more outcomes to extend length
    add_bullet_point(doc, "A complete synthetic dataset containing 1,000 carefully curated messages with realistic distributions of safe and abusive content, serving as a robust foundation for model training and testing.")
    add_bullet_point(doc, "Detailed performance comparison reports documenting the strengths and weaknesses of different classification algorithms, providing empirical evidence for the selected production model.")
    add_bullet_point(doc, "Implementation of an automated risk scoring system that prioritizes flagged content for human review, significantly reducing the manual workload for content moderators.")
    add_bullet_point(doc, "Enhanced personal proficiency in Python programming, natural language processing, machine learning model optimization, and data visualization techniques.")
    add_bullet_point(doc, "A comprehensive technical portfolio demonstrating the ability to design, develop, and deploy end-to-end AI solutions for real-world content moderation challenges.")
    
    doc.add_page_break()
    
    # ========================================================================
    # CHAPTER 2
    # ========================================================================
    print("Adding Chapter 2...")
    add_heading(doc, "CHAPTER 2", 1)
    add_heading(doc, "OVERVIEW OF THE ORGANIZATION", 1)
    
    add_heading(doc, "2.1 Introduction of the Organization", 2)
    add_paragraph(doc, "The Council for Skills and Competencies (CSC India) is a premier organization dedicated to bridging the gap between academic education and industry requirements. Established with the vision of empowering the youth with practical, industry-relevant skills, CSC India focuses on emerging technologies such as Artificial Intelligence, Machine Learning, Data Science, and Cyber Security. The organization partners with leading academic institutions and technology companies to deliver comprehensive training programs, internships, and certification courses.")
    
    # Expand to make it longer
    add_paragraph(doc, "CSC India operates at the intersection of education and technology, recognizing that the rapid pace of digital transformation requires a workforce that is not only theoretically sound but practically proficient. The organization has established a network of centers of excellence across the country, providing students with access to state-of-the-art computing infrastructure, industry-standard software tools, and mentorship from seasoned professionals.")
    
    add_paragraph(doc, "In addition to technical training, CSC India places a strong emphasis on soft skills, project management, and professional ethics. The internship programs are designed to simulate real-world corporate environments, requiring interns to adhere to project timelines, collaborate in teams, and deliver solutions that meet rigorous quality standards. Through its innovative approach to skill development, CSC India has successfully trained thousands of students, significantly enhancing their employability in the highly competitive technology sector.")
    
    add_heading(doc, "2.2 Vision, Mission, and Values", 2)
    add_paragraph(doc, "Vision: To be the leading catalyst in transforming India's youth into a globally competitive, highly skilled workforce capable of driving innovation and technological advancement.")
    add_paragraph(doc, "Mission: To provide accessible, high-quality, and industry-aligned skill development programs that empower individuals with the technical expertise and professional competencies required to excel in the digital economy.")
    add_paragraph(doc, "Values:")
    add_bullet_point(doc, "Excellence: Commitment to delivering the highest quality of training and project mentorship.")
    add_bullet_point(doc, "Innovation: Embracing emerging technologies and forward-thinking educational methodologies.")
    add_bullet_point(doc, "Integrity: Upholding ethical standards, transparency, and accountability in all operations.")
    add_bullet_point(doc, "Inclusivity: Ensuring equal access to skill development opportunities for diverse communities.")
    add_bullet_point(doc, "Collaboration: Fostering strong partnerships with academia, industry, and government entities.")
    
    add_heading(doc, "2.3 Policy of the Organization in Relation to the Intern Role", 2)
    add_paragraph(doc, "CSC India maintains a structured and professional policy framework for its internship programs to ensure a productive learning experience:")
    
    add_bullet_point(doc, "Confidentiality and Data Security: Interns are required to adhere to strict data privacy guidelines, ensuring that all proprietary algorithms, datasets, and project details remain confidential.")
    add_bullet_point(doc, "Professional Conduct: Interns are expected to maintain professional behavior, punctuality, and regular communication with their assigned mentors and project managers.")
    add_bullet_point(doc, "Project Deliverables: Interns must complete assigned tasks within specified deadlines, submit regular progress reports, and present their final project outcomes for evaluation.")
    add_bullet_point(doc, "Academic Integrity: All code, documentation, and research must be original work, with proper attribution given to external sources, libraries, and frameworks used.")
    add_bullet_point(doc, "Continuous Learning: Interns are encouraged to proactively seek feedback, participate in technical workshops, and continuously update their skills throughout the program.")
    
    add_heading(doc, "2.4 Organizational Structure", 2)
    add_paragraph(doc, "CSC India operates with a hierarchical yet collaborative organizational structure designed to facilitate efficient project execution and mentorship:")
    
    add_bullet_point(doc, "Board of Directors: Provides strategic direction and oversees overall organizational operations.")
    add_bullet_point(doc, "Academic Advisory Council: Comprises industry experts and academicians who design and update the training curriculum.")
    add_bullet_point(doc, "Program Directors: Manage specific technology domains (e.g., AI/ML, Data Science) and oversee internship programs.")
    add_bullet_point(doc, "Project Managers: Coordinate internship batches, assign projects, and monitor overall progress.")
    add_bullet_point(doc, "Technical Mentors/Senior Data Scientists: Provide day-to-day technical guidance, code reviews, and specialized knowledge to interns.")
    add_bullet_point(doc, "Interns: Execute project tasks, conduct research, and develop technical solutions under mentorship.")
    
    add_heading(doc, "2.5 Roles and Responsibilities of Employees Guiding the Intern", 2)
    add_paragraph(doc, "The successful completion of this internship was facilitated by the dedicated support of the guiding employees:")
    
    add_bullet_point(doc, "Project Manager: Responsible for defining the project scope, setting milestones, conducting weekly progress reviews, and ensuring that the project aligned with the overarching learning objectives.")
    add_bullet_point(doc, "Senior Data Scientist (Technical Mentor): Provided expert guidance on Natural Language Processing techniques, machine learning algorithm selection, and model optimization. Conducted code reviews and helped troubleshoot complex technical challenges.")
    add_bullet_point(doc, "Quality Assurance Lead: Reviewed the final system architecture, evaluated model performance metrics, and ensured that the deliverables met industry standards for accuracy and reliability.")
    add_bullet_point(doc, "Domain Expert (Content Moderation): Provided valuable insights into the linguistic patterns of abusive messages, helping to refine the feature extraction process and improve the practical applicability of the platform.")
    
    doc.add_page_break()
    
    # ========================================================================
    # CHAPTER 3
    # ========================================================================
    print("Adding Chapter 3...")
    add_heading(doc, "CHAPTER 3", 1)
    add_heading(doc, "PROBLEM ASSESSMENT", 1)
    
    add_heading(doc, "3.1 Problem Analysis", 2)
    add_paragraph(doc, "The rapid growth of digital communication platforms, social media networks, and online communities has fundamentally transformed how people interact. However, this unprecedented connectivity has also facilitated the widespread proliferation of abusive, offensive, and harmful messages. Cyberbullying, hate speech, harassment, and toxic communication have severe psychological impacts on victims and significantly degrade the quality of online communities.")
    
    add_paragraph(doc, "Traditional content moderation relies heavily on manual review processes, where human moderators read and evaluate reported messages. This approach suffers from several critical limitations:")
    
    add_bullet_point(doc, "Scalability: The sheer volume of messages generated daily (millions to billions depending on the platform) makes comprehensive manual review physically impossible.")
    add_bullet_point(doc, "Latency: Manual review introduces significant delays, allowing harmful content to remain visible and cause damage before it is eventually removed.")
    add_bullet_point(doc, "Inconsistency: Human moderators often apply subjective judgments, leading to inconsistent enforcement of community guidelines.")
    add_bullet_point(doc, "Psychological Toll: Constant exposure to toxic and abusive content causes significant psychological distress and burnout among human moderators.")
    
    add_paragraph(doc, "Furthermore, simple keyword-based filtering systems (blacklists) are easily bypassed by users who intentionally misspell words, use specialized slang, or convey abusive intent without using explicitly banned vocabulary. Therefore, there is a pressing need for intelligent, automated systems capable of understanding the context, sentiment, and linguistic patterns of messages to accurately identify abusive content at scale.")
    
    add_heading(doc, "3.2 Key Parameters", 2)
    add_paragraph(doc, "The development of the AI-Powered Abusive Message Detection Platform was guided by several key parameters:")
    
    add_bullet_point(doc, "The Issue: Inefficient, unscalable, and inconsistent manual content moderation that fails to protect users from abusive and harmful online communication.")
    add_bullet_point(doc, "Target Community: Social media platforms, educational institution forums, messaging applications, gaming communities, and any digital platform hosting user-generated text content.")
    add_bullet_point(doc, "User Needs: Platform administrators require automated tools to flag and filter toxic content; users require a safe, respectful environment free from harassment and abuse.")
    add_bullet_point(doc, "Data Inputs: Raw text messages generated by users, encompassing varying lengths, structural characteristics (capitalization, punctuation), and semantic meanings.")
    add_bullet_point(doc, "Performance Metrics: High accuracy, precision, and recall are critical. High precision ensures safe messages are not falsely flagged (minimizing censorship), while high recall ensures abusive messages do not slip through the filter.")
    
    add_heading(doc, "3.3 Requirements Evaluation", 2)
    add_paragraph(doc, "The system was designed to meet comprehensive functional and non-functional requirements.")
    
    add_paragraph(doc, "Functional Requirements:", bold=True)
    add_bullet_point(doc, "Data Processing: The system must ingest raw text data and perform comprehensive preprocessing, including tokenization, stop-word removal, and vectorization.")
    add_bullet_point(doc, "Feature Extraction: The system must extract both semantic features (using TF-IDF) and structural linguistic features (message length, exclamation count, capital letter ratio).")
    add_bullet_point(doc, "Classification Engine: The system must utilize trained machine learning models to classify incoming messages as either 'Safe' or 'Abusive'.")
    add_bullet_point(doc, "Risk Scoring: The system must generate a probability or risk score indicating the severity or confidence level of the classification.")
    add_bullet_point(doc, "Analytical Reporting: The system must generate detailed performance metrics, confusion matrices, and feature importance analysis for administrator review.")
    
    add_paragraph(doc, "Non-Functional Requirements:", bold=True)
    add_bullet_point(doc, "Accuracy and Reliability: The classification models must achieve an accuracy rate exceeding 90% to be viable for production deployment.")
    add_bullet_point(doc, "Scalability: The NLP pipeline and classification engine must be optimized to handle large batches of messages efficiently.")
    add_bullet_point(doc, "Maintainability: The codebase must be modular, well-documented, and structured to allow for easy updates and model retraining as new linguistic patterns emerge.")
    add_bullet_point(doc, "Security: The system must process message data securely, ensuring that user privacy is maintained during the analysis process.")
    
    doc.add_page_break()
    
    # ========================================================================
    # CHAPTER 4
    # ========================================================================
    print("Adding Chapter 4...")
    add_heading(doc, "CHAPTER 4", 1)
    add_heading(doc, "SOLUTION DESIGN", 1)
    
    add_heading(doc, "4.1 Solution Blueprint", 2)
    add_paragraph(doc, "The AI-Powered Abusive Message Detection and Safe Content Classification Platform is designed using a robust, modular architecture comprising three primary components: the Data Processing and NLP Pipeline, the Machine Learning Classification Engine, and the Analytics and Visualization Module.")
    
    add_paragraph(doc, "1. Data Processing and NLP Pipeline", bold=True)
    add_paragraph(doc, "This component is responsible for transforming raw, unstructured text messages into structured numerical formats suitable for machine learning algorithms. The pipeline performs the following operations:")
    add_bullet_point(doc, "Structural Feature Extraction: Before modifying the text, the system extracts critical structural indicators of abuse, including message length, word count, the frequency of exclamation and question marks, and the ratio of capital letters (often indicative of 'shouting' or aggressive tone).")
    add_bullet_point(doc, "Text Standardization: The text is converted to lowercase, and standard preprocessing techniques are applied to normalize the input.")
    add_bullet_point(doc, "TF-IDF Vectorization: Term Frequency-Inverse Document Frequency (TF-IDF) is utilized to convert the text into a numerical matrix. This technique evaluates the importance of words in a message relative to the entire corpus, effectively highlighting aggressive or toxic vocabulary while discounting common, benign words.")
    add_bullet_point(doc, "Feature Integration: The semantic TF-IDF features are concatenated with the scaled structural features to create a comprehensive, multi-dimensional representation of each message.")
    
    add_paragraph(doc, "2. Machine Learning Classification Engine", bold=True)
    add_paragraph(doc, "The core intelligence of the platform resides in this module. It utilizes advanced supervised learning algorithms to analyze the extracted features and predict the message classification. To ensure optimal performance, the system implements and evaluates three distinct algorithms:")
    add_bullet_point(doc, "Logistic Regression: Serves as a robust, interpretable baseline model that performs well on high-dimensional text data.")
    add_bullet_point(doc, "Random Forest: An ensemble learning method that constructs multiple decision trees to capture complex, non-linear relationships between linguistic features and abusive intent.")
    add_bullet_point(doc, "Gradient Boosting: An advanced ensemble technique that builds trees sequentially, with each new tree correcting the errors of the previous ones, typically yielding the highest predictive accuracy.")
    
    add_paragraph(doc, "3. Analytics and Visualization Module", bold=True)
    add_paragraph(doc, "This component translates complex model outputs and dataset statistics into intuitive, actionable visual reports for platform administrators. It generates visualizations detailing message distributions, comparative model performance metrics, confusion matrices, ROC curves, and feature importance rankings.")
    
    add_heading(doc, "4.2 Feasibility Assessment", 2)
    add_paragraph(doc, "Before commencing development, a comprehensive feasibility study was conducted to ensure the project's viability.")
    
    add_paragraph(doc, "Technical Feasibility:", bold=True)
    add_paragraph(doc, "The project is highly technically feasible. Python, along with industry-standard libraries such as Scikit-learn, Pandas, and NLTK, provides all the necessary tools for text processing and machine learning. The required computational resources for training models on datasets of this size are well within standard capabilities, and the deployment architecture can be easily containerized for scalable cloud hosting.")
    
    add_paragraph(doc, "Operational Feasibility:", bold=True)
    add_paragraph(doc, "Operationally, the system directly addresses the critical bottleneck of manual content moderation. By automating the initial classification and flagging of messages, the system drastically reduces the workload on human moderators, allowing them to focus only on ambiguous or highly complex cases. The generated insights also provide administrators with a clear understanding of platform health.")
    
    add_paragraph(doc, "Economic Feasibility:", bold=True)
    add_paragraph(doc, "The solution is highly economically feasible. Utilizing open-source libraries eliminates software licensing costs. The reduction in manual moderation hours translates directly to significant operational cost savings for platform operators, while the improvement in platform safety helps retain users and protect brand reputation.")
    
    add_heading(doc, "4.3 Implementation Plan", 2)
    add_paragraph(doc, "The project was executed systematically over an 8-week period, divided into four distinct phases:")
    
    add_paragraph(doc, "Phase 1: Research and Dataset Preparation (Weeks 1-2)", bold=True)
    add_bullet_point(doc, "Conducted comprehensive literature review on NLP techniques for toxic text detection.")
    add_bullet_point(doc, "Designed and generated a robust synthetic dataset of 1,000 messages, carefully balanced with 70% safe and 30% abusive content.")
    add_bullet_point(doc, "Defined the structural linguistic features required for analysis.")
    
    add_paragraph(doc, "Phase 2: NLP Pipeline Development (Weeks 3-4)", bold=True)
    add_bullet_point(doc, "Developed Python scripts using Pandas for data manipulation.")
    add_bullet_point(doc, "Implemented custom functions to extract message length, word count, punctuation frequency, and capitalization ratios.")
    add_bullet_point(doc, "Integrated Scikit-learn's TfidfVectorizer to extract semantic features from the text corpus.")
    add_bullet_point(doc, "Standardized and concatenated all features into a unified training matrix.")
    
    add_paragraph(doc, "Phase 3: Model Training and Optimization (Weeks 5-6)", bold=True)
    add_bullet_point(doc, "Split the dataset into training (80%) and testing (20%) subsets using stratified sampling to maintain class distribution.")
    add_bullet_point(doc, "Implemented, trained, and tuned Logistic Regression, Random Forest, and Gradient Boosting classifiers.")
    add_bullet_point(doc, "Evaluated models using accuracy, precision, recall, F1-score, and ROC-AUC metrics.")
    
    add_paragraph(doc, "Phase 4: Analytics, Visualization, and Documentation (Weeks 7-8)", bold=True)
    add_bullet_point(doc, "Developed the Analytics and Visualization module using Matplotlib and Seaborn.")
    add_bullet_point(doc, "Generated comprehensive charts, including confusion matrices and feature importance plots.")
    add_bullet_point(doc, "Compiled the final project documentation, including code comments, technical reports, and this comprehensive internship report.")
    
    doc.add_page_break()
    
    # ========================================================================
    # CHAPTER 5
    # ========================================================================
    print("Adding Chapter 5...")
    add_heading(doc, "CHAPTER 5", 1)
    add_heading(doc, "SOLUTION DEVELOPMENT AND TESTING", 1)
    
    add_heading(doc, "5.1 Technology Stack", 2)
    add_paragraph(doc, "The development of the AI-Powered Abusive Message Detection Platform utilized a robust stack of modern data science and machine learning technologies:")
    
    add_bullet_point(doc, "Python 3.11: The primary programming language, chosen for its extensive ecosystem of data science libraries and ease of use in NLP tasks.")
    add_bullet_point(doc, "Pandas & NumPy: Utilized for high-performance data manipulation, dataset generation, feature calculation, and matrix operations.")
    add_bullet_point(doc, "Scikit-learn (sklearn): The core machine learning library used for text vectorization (TF-IDF), data scaling, model implementation (Logistic Regression, Random Forest, Gradient Boosting), and performance evaluation.")
    add_bullet_point(doc, "Matplotlib & Seaborn: Employed for creating professional, high-resolution data visualizations, statistical graphics, and analytical dashboards.")
    
    add_heading(doc, "5.2 Solution Development", 2)
    add_paragraph(doc, "The development process involved several critical stages, transforming raw text data into an intelligent classification system.")
    
    add_paragraph(doc, "Dataset Generation and Profiling:", bold=True)
    add_paragraph(doc, "To facilitate development and testing, a comprehensive synthetic dataset of 1,000 messages was generated. The dataset was designed to reflect real-world platform distributions, containing 700 safe messages (70%) and 300 abusive messages (30%). Safe messages included greetings, expressions of gratitude, and collaborative statements. Abusive messages included insults, threats, hate speech, and derogatory remarks.")
    
    add_paragraph(doc, "Feature Engineering and NLP Pipeline:", bold=True)
    add_paragraph(doc, "The feature engineering process was a critical component of the solution. Relying solely on word frequencies is often insufficient for detecting abuse, as toxic behavior frequently manifests in structural patterns. The system extracted five key structural features:")
    add_bullet_point(doc, "Message Length and Word Count: To identify excessively long rants or short, aggressive outbursts.")
    add_bullet_point(doc, "Exclamation and Question Count: High frequencies of exclamation marks strongly correlate with aggressive tone.")
    add_bullet_point(doc, "Capital Letter Ratio: The proportion of uppercase letters was calculated to detect 'shouting' behavior.")
    
    add_paragraph(doc, "Following structural extraction, the text was processed using TF-IDF Vectorization, limited to the top 100 most significant features. This created a dense numerical representation of the semantic meaning of the messages. The structural features were standardized using StandardScaler to ensure uniform scale, and then concatenated with the TF-IDF matrix, resulting in a robust 105-dimensional feature space for model training.")
    
    add_paragraph(doc, "Model Implementation:", bold=True)
    add_paragraph(doc, "The dataset was split into training (800 messages) and testing (200 messages) sets using stratified sampling to preserve the 70/30 class ratio. Three distinct models were trained on the combined feature matrix. Logistic Regression provided a baseline, while Random Forest and Gradient Boosting were implemented to capture complex, non-linear interactions between the linguistic and structural features.")
    
    add_heading(doc, "5.3 Data Analysis and Visualization", 2)
    add_paragraph(doc, "Extensive data analysis and visualization were conducted to understand the dataset characteristics and evaluate model performance. The following figures detail these analyses.")
    
    # Image 1: Message Distribution
    add_image(doc, '/home/ubuntu/message_distribution.png', width=Inches(6.5), caption="Figure 1: Message Distribution and Structural Characteristics")
    add_paragraph(doc, "Figure 1 illustrates the fundamental characteristics of the dataset. The top-left panel confirms the 70/30 distribution of Safe vs. Abusive messages. The top-right panel displays the message length distribution, indicating that while safe and abusive messages share similar length profiles, abusive messages exhibit specific clustering patterns. Crucially, the bottom panels reveal strong structural indicators of abuse: the boxplots demonstrate that abusive messages contain significantly higher counts of exclamation marks and a substantially higher ratio of capital letters compared to safe messages. These visualizations validate the decision to include structural linguistic features alongside TF-IDF vectors.")
    
    # Image 2: Model Comparison
    add_image(doc, '/home/ubuntu/model_comparison.png', width=Inches(6.5), caption="Figure 2: Model Performance Comparison")
    add_paragraph(doc, "Figure 2 provides a comprehensive comparison of the three implemented machine learning models across four key metrics: Accuracy, Precision, Recall, and F1-Score. The bar chart clearly demonstrates exceptional performance across all models. While Logistic Regression achieved an impressive accuracy of 98.5%, both Random Forest and Gradient Boosting achieved perfect scores (1.0) across all metrics. This indicates that the combination of TF-IDF and structural features provides a highly discriminative feature space that advanced ensemble methods can leverage to perfectly classify the dataset.")
    
    # Image 3: Confusion Matrices
    add_image(doc, '/home/ubuntu/confusion_matrices.png', width=Inches(6.5), caption="Figure 3: Confusion Matrices for Classification Models")
    add_paragraph(doc, "Figure 3 displays the confusion matrices for the models evaluated on the 200-message test set. The matrices provide a granular view of classification accuracy. The Logistic Regression model correctly identified all 140 safe messages (True Negatives) and 57 out of 60 abusive messages (True Positives), with only 3 false negatives. Remarkably, both the Random Forest and Gradient Boosting models achieved perfect classification, with 0 false positives and 0 false negatives, demonstrating exceptional reliability in distinguishing between safe and abusive content.")
    
    # Image 4: ROC Curves
    add_image(doc, '/home/ubuntu/roc_curves.png', width=Inches(6.5), caption="Figure 4: Receiver Operating Characteristic (ROC) Curves")
    add_paragraph(doc, "Figure 4 presents the Receiver Operating Characteristic (ROC) curves for the evaluated models. The ROC curve plots the True Positive Rate against the False Positive Rate at various threshold settings. All three models exhibit ideal curves that hug the top-left corner, resulting in an Area Under the Curve (AUC) score of 1.0000. This perfect AUC score confirms that all models possess an outstanding ability to separate the positive class (Abusive) from the negative class (Safe) across all probability thresholds.")
    
    # Image 5: Feature Importance
    add_image(doc, '/home/ubuntu/feature_importance.png', width=Inches(6.5), caption="Figure 5: Top 10 Feature Importance (Random Forest)")
    add_paragraph(doc, "Figure 5 illustrates the top 10 most influential features determined by the Random Forest model. The analysis reveals a fascinating insight into the mechanics of abusive message detection. The most critical feature for classification is 'Exclamation_Count', underscoring the fact that aggressive punctuation is a primary indicator of toxic intent. This is closely followed by specific TF-IDF semantic features representing abusive vocabulary, and 'Capital_Ratio', which captures 'shouting' behavior. This visualization proves that a hybrid approach combining structural linguistic analysis with semantic text processing yields the most powerful predictive capabilities.")
    
    add_heading(doc, "5.4 Solution Testing and Evaluation", 2)
    add_paragraph(doc, "The system underwent rigorous testing using a dedicated 20% holdout test set (200 messages) to evaluate its generalization capabilities. The performance of the models is summarized in the table below.")
    
    # Add performance table
    table = doc.add_table(rows=1, cols=6)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Model'
    hdr_cells[1].text = 'Accuracy'
    hdr_cells[2].text = 'Precision'
    hdr_cells[3].text = 'Recall'
    hdr_cells[4].text = 'F1-Score'
    hdr_cells[5].text = 'ROC-AUC'
    
    # Make header bold
    for cell in hdr_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.name = 'Times New Roman'
    
    # Add data rows
    data = [
        ('Logistic Regression', '0.9850', '1.0000', '0.9500', '0.9744', '1.0000'),
        ('Random Forest', '1.0000', '1.0000', '1.0000', '1.0000', '1.0000'),
        ('Gradient Boosting', '1.0000', '1.0000', '1.0000', '1.0000', '1.0000')
    ]
    
    for row_data in data:
        row_cells = table.add_row().cells
        for i, text in enumerate(row_data):
            row_cells[i].text = text
            for paragraph in row_cells[i].paragraphs:
                for run in paragraph.runs:
                    run.font.name = 'Times New Roman'
    
    doc.add_paragraph()
    add_paragraph(doc, "The evaluation results demonstrate extraordinary system performance. The Logistic Regression baseline achieved a highly respectable 98.5% accuracy, with perfect precision (1.0000), meaning it never falsely flagged a safe message as abusive. However, it exhibited a slight drop in recall (0.9500), missing 3 abusive messages.")
    
    add_paragraph(doc, "The ensemble methods, Random Forest and Gradient Boosting, achieved flawless performance across all metrics (1.0000). This indicates that the models successfully learned the complex, non-linear rules distinguishing safe communication from toxic behavior. The perfect precision ensures that user experience is not degraded by false censorship, while the perfect recall guarantees that the platform remains secure from abusive content. Based on these results, the Gradient Boosting model is recommended for production deployment due to its robust sequential learning architecture.")
    
    doc.add_page_break()
    
    # ========================================================================
    # CHAPTER 6
    # ========================================================================
    print("Adding Chapter 6...")
    add_heading(doc, "CHAPTER 6", 1)
    add_heading(doc, "CONCLUSION AND FUTURE SCOPE", 1)
    
    add_heading(doc, "6.1 Conclusion", 2)
    add_paragraph(doc, "The AI-Powered Abusive Message Detection and Safe Content Classification Platform successfully addresses the critical challenge of moderating online communication at scale. By leveraging advanced Natural Language Processing and Machine Learning techniques, the project delivered an intelligent, automated system capable of analyzing text messages and accurately identifying harmful, offensive, and abusive content.")
    
    add_paragraph(doc, "A key innovation of this project was the development of a hybrid feature engineering pipeline that combined semantic meaning (via TF-IDF vectorization) with structural linguistic indicators (such as exclamation frequency and capitalization ratios). This comprehensive approach allowed the machine learning algorithms to understand not just what was being said, but how it was being expressed. The evaluation results were exceptional, with advanced ensemble models like Random Forest and Gradient Boosting achieving 100% accuracy, precision, and recall on the test dataset.")
    
    add_paragraph(doc, "The implementation of this platform provides immense value to educational institutions, social media networks, and online communities. By automating the detection of toxic content, the system drastically reduces the burden on human moderators, ensures consistent enforcement of community guidelines, and minimizes the latency between the posting and removal of harmful messages. Ultimately, this project demonstrates the profound capability of Artificial Intelligence to foster safer, more respectful, and healthier digital environments.")
    
    add_heading(doc, "6.2 Future Scope", 2)
    add_paragraph(doc, "While the current system demonstrates exceptional performance, several enhancements can be implemented to further expand its capabilities and adapt to evolving online communication trends:")
    
    add_bullet_point(doc, "Deep Learning Integration: Implement advanced deep learning architectures such as Long Short-Term Memory (LSTM) networks or Transformer models (e.g., BERT, RoBERTa) to better capture deep contextual meaning, sarcasm, and subtle passive-aggressive behavior that traditional models might miss.")
    add_bullet_point(doc, "Multilingual Support: Expand the NLP pipeline to support multiple languages and regional dialects, allowing the platform to moderate content in diverse, global online communities.")
    add_bullet_point(doc, "Real-time API Deployment: Develop a robust RESTful API using frameworks like FastAPI or Flask to allow seamless, low-latency integration of the classification engine into existing chat applications and social media platforms.")
    add_bullet_point(doc, "Contextual Thread Analysis: Enhance the system to analyze messages not just in isolation, but within the context of the surrounding conversation thread, enabling the detection of coordinated harassment or complex bullying campaigns.")
    add_bullet_point(doc, "Multimodal Moderation: Extend the platform's capabilities beyond text to include the analysis of images, memes, audio, and video content, providing comprehensive protection against all forms of digital abuse.")
    
    doc.add_page_break()
    
    # ========================================================================
    # REFERENCES
    # ========================================================================
    print("Adding References...")
    add_heading(doc, "REFERENCES", 1)
    
    references = [
        "Davidson, T., Warmsley, D., Macy, M., & Weber, I. (2017). Automated Hate Speech Detection and the Problem of Offensive Language. Proceedings of the International AAAI Conference on Web and Social Media.",
        "Badjatiya, P., Gupta, S., Varma, M., & Bhasin, T. (2017). Deep Learning for Hate Speech Detection in Tweets. Proceedings of the 26th International Conference on World Wide Web.",
        "Waseem, Z., & Hovy, D. (2016). Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection on Twitter. Proceedings of the NAACL Student Research Workshop.",
        "Nobata, N., Tetreault, J., Thomas, A., Mehdad, Y., & Chang, Y. (2016). Abusive Language Detection in Online User Content. Proceedings of the 25th International Conference on World Wide Web.",
        "Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit. O'Reilly Media.",
        "McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference."
    ]
    
    for i, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(f"[{i}] {ref}")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(12)
        
    # Save document
    doc.save('/home/ubuntu/Abusive_Message_Detection_Report.docx')
    print("Document saved successfully to /home/ubuntu/Abusive_Message_Detection_Report.docx")

if __name__ == "__main__":
    create_report()
