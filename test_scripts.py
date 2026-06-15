TEST_SCRIPTS = [
    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer's internet dropped during a critical meeting. They are stressed and frantic.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Frustrated]</span><br/>
Hi, I'm calling because I've been trying to log into my account for the last three days and it's completely locked me out. I've reset my password twice already, and every single time it tells me my credentials are invalid. This is incredibly unacceptable, I need access to my billing statements right now!<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Confused]</span><br/>
Wait... I'm looking at the email you just sent. It says my account is linked to a different email address? How is that even possible? I've only ever used one email for this service.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Relieved]</span><br/>
Oh, I see. My spouse set up the family plan and used their work email. Okay, that makes sense. I'm really sorry for getting upset earlier.""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer is inquiring about upgrading software but discovers a compatibility issue.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Cheerful]</span><br/>
Good morning! I was calling because I saw your new premium software features advertised, and I am absolutely thrilled about the new integration options. I'd love to upgrade today.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Disappointed]</span><br/>
Oh, you're saying the new integration tools aren't available for Mac users yet? That's really disappointing. The website didn't make that clear at all.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Resigned]</span><br/>
Well, I suppose I could run it on a virtual machine for now. Do you have a timeline for when the Mac version will be released?""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer notices a huge unauthorized charge on their bank account.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Anxious]</span><br/>
Hello, yes, this is an emergency. I just received a notification that a payment of $800 was processed from my checking account, and I definitely did not authorize this!<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Confused]</span><br/>
Wait, you're saying this was for an annual renewal? But I cancelled my subscription three months ago! Why would I be charged for a renewal?<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Apologetic]</span><br/>
Ah... I cancelled the wrong software package? Wow, okay. That is entirely my mistake. Is there any possibility of a prorated refund if I cancel it completely right now?""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer receives a strange package they did not order.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Confused]</span><br/>
Hi there, I received a package in the mail today from your company, but I didn't order anything. It's a huge box of replacement filters.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Annoyed]</span><br/>
What do you mean you can't generate a return label unless I provide an order number? I just told you I didn't order this! I'm not paying for shipping to return something I never bought.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Professional]</span><br/>
Oh, it was a gift sent by my sister? Well, that changes things. Okay, please don't cancel it, I'll call her. Sorry for the confusion.""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: IT Manager calling to get specific technical details before a bulk purchase.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Professional]</span><br/>
Good afternoon. I'm calling to inquire about the technical specifications of your enterprise router, specifically regarding the maximum throughput when all security protocols are enabled.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Frustrated]</span><br/>
Yes, I understand you have a spec sheet on the website, I've already read it. It doesn't answer my question about the IPSec tunnel overhead. I need to speak to an actual sales engineer immediately.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Impressed]</span><br/>
Ah, you're the engineer. Excellent. Okay, those numbers you just cited are actually much better than I anticipated. Could you send me a formal quote for 50 units?""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer leaving feedback on a fitness app they love but found a bug in.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Cheerful]</span><br/>
Hey! I'm just calling to leave some feedback. I've been using your fitness app for the last six months, and honestly, it's completely changed my routine. The UI is beautiful!<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Analytical]</span><br/>
However, I did want to mention a small bug. When you try to log a custom workout that spans past midnight, the app splits it into two different days and completely ruins the weekly streak counter.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Constructive]</span><br/>
If your dev team could add an option to manually assign the workout to a specific calendar day, that would completely solve the problem. Keep up the great work overall!""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer trying to cancel service but hit with an unexpected fee.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Aggressive]</span><br/>
I want to cancel my service right now. Do not try to offer me any discounts, just close the account. Your service is terrible.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Hesitant]</span><br/>
Wait, what do you mean there's a $200 early termination fee? I only signed up three months ago, the salesperson told me there was no contract! This is a complete scam.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Negotiating]</span><br/>
Okay... so if I downgrade to the basic plan, the contract extends, but there's no cancellation fee? Fine. Just downgrade it for now. I'll ride out the rest of the contract.""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer spots a weird charge but realizes their kid made an in-app purchase.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Curious]</span><br/>
Hi, I saw a charge on my credit card for $12.99 from your company, but the description is just a bunch of random letters. What is this extra charge for?<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Amused]</span><br/>
Oh, really? It was for premium avatar outfits? Haha, my ten-year-old son must have bought those while playing on my tablet.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Firm]</span><br/>
Alright, well, I won't dispute the charge this time. But can you please show me how to set up a PIN code for any future purchases? I need to make sure he can't go on a shopping spree.""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer panicking after their dog ate gardening fertilizer.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Hesitant]</span><br/>
Hi... um, I think my dog might have eaten some of the fertilizer I bought from your gardening center. He's acting really lethargic. Is this stuff toxic to pets?<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Panicked]</span><br/>
It contains what?! Oh my god. Okay, I'm grabbing my keys right now. Is there anything I should do on the way? Should I try to induce vomiting again?<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Focused]</span><br/>
No, okay, just get to the vet immediately. Understood. Thank you for checking the poison control database for me, I'm hanging up now to drive.""",

    """<span style="font-size: 0.9rem; font-style: italic; color: #9B7EBD;">[Background: Customer fighting a Homeowners Association fine about their door color.]</span><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Starts Formal]</span><br/>
To whom it may concern, I am calling to officially dispute a violation notice I received regarding the paint color of my front door. I submitted the required paperwork six weeks ago.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Frustrated]</span><br/>
The architectural committee lost my paperwork? That is not my problem. I painted it a pre-approved color. I will not be repainting it, and I refuse to pay the fine.<br/><br/>
<span style="font-size: 0.8rem; font-style: italic; color: #9B7EBD;">[Tone: Shifts to Satisfied]</span><br/>
Finally, some common sense. Yes, please waive the fine and update your records. I can email you a copy of the original request form if you need it. Thank you."""
]
