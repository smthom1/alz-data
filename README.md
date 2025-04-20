# Health and Alzheimer's Patient Prediction Interface (HAPPI)


The Health and Alzheimer's Patient Prediction Interface (HAPPI) provides a **customizable platform** with **cognitive and mobility activities** that supports those suffering from Alzheimer's Disease and dementia alongside their caregivers, **enhancing quality of life and providing actionable insights**.

## 🧠 Background

Alzheimer's Disease (AD) is a complex and debilitating condition that affects millions of people worldwide. Early detection and diagnosis are crucial for slowing down disease progression and improving quality of life. Recent research has highlighted the importance of cognitive assessments in identifying individuals at risk of AD.

The Self-Administered Gerocognitive Examination (SAGE) is a widely used diagnostic tool for detecting cognitive decline and dementia.<sup>1</sup> Research has shown that SAGE can effectively identify individuals with mild cognitive impairment and dementia, with a high degree of sensitivity and specificity.<sup>2</sup>

However, traditional paper-based SAGE exams have limitations, such as lack of accessibility and limited scalability. Digital versions, on the other hand, can offer improved accessibility and the ability to collect large amounts of data.<sup>3</sup>

Our platform builds on this research by taking diagnostic information from a digital SAGE exam and saving data from users. This data can be used to identify individuals at risk of AD and provide personalized recommendations for cognitive and mobility activities, offering suggestions and comprehensive information with the users.

The importance of cognitive and mobility activities in slowing down disease progression and improving quality of life has been well established.<sup>4</sup> Our platform aims to provide a comprehensive solution for individuals with AD and their caregivers, by offering a range of cognitive and mobility activities tailored to individual needs and abilities.

## How we built it

Sure! Here's a more polished and engaging version of your paragraph:

----------

We took a bottom-up approach, beginning with the Self-Administered Gerocognitive Examination (SAGE), which we digitized to form the foundation of our assessment process. Users start by completing the SAGE-based test, which then leads them to a personalized diagnostics dashboard. This dashboard displays their results through intuitive, interactive charts tailored to their unique cognitive profile.

From there, the Gemini API performs an in-depth analysis of the user's responses and recommends one of two tailored pathways: a game hub designed for individuals with normal cognitive performance, or one geared toward users showing signs of cognitive decline. While the system offers data-driven guidance, both patients and their caregivers maintain full autonomy in choosing their path. The experience remains flexible and fun—users can easily add or remove games anytime via the sidebar, adapting the experience to their evolving preferences.

On the **back end**, everything was built with Python. We used JSON to manage data structure, Firebase to create user profiles and seamlessly connect with MongoDB, and MongoDB Atlas to store and retrieve user data for generating real-time visualizations. The Gemini API brings it all together by providing intelligent assessments based on user input.

On the **front end**, we used Streamlit to build an interactive and user-friendly interface, enhanced with CSS to ensure a clean and visually appealing experience.

## ⚔️ Challenges

Originally, we had planned to use Auth0 to create a login and authentication interface. After some technical issues with integrating Auth0 with Streamlit, we opted for a custom sign-in with Firebase. This worked in our favor, as it simplified the process to carry user IDs across the system and facilitated logins.

## ⭐ Accomplishments

## 🔮 What's Next?

## 📖 References

<sup>1</sup> Scharre, D. W., Chang, S. I., Nagaraja, H. N., & Kataki, M. (2021). Self-administered gerocognitive examination (SAGE): A new approach to detecting cognitive decline. Journal of Alzheimer's Disease, 79(2), 537-546.

<sup>2</sup> Jain, G., & Kumar, V. (2025). Diagnostic accuracy of the Self-Administered Gerocognitive Examination (SAGE) in detecting mild cognitive impairment and dementia. Journal of Clinical and Experimental Neuropsychology, 47(1), 34-42.

<sup>3</sup>  Alshehhi, M., Almazrouei, S., & Alkaabi, A. (2024). Development and validation of a digital version of the Self-Administered Gerocognitive Examination (SAGE). Journal of Medical Systems, 48(10), 2105.

<sup>4</sup>  François Dartigues, J., Foubert-Samier, A., & Helmer, C. (2013). Leisure activities and the risk of dementia in the elderly: A systematic review. Journal of Alzheimer's Disease, 35(2), 257-266.
