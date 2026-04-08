#!/usr/bin/env python3
"""
Generate complaints for all products in the catalog.
Generates 40-50 complaints per product with realistic defects based on product type.
"""
import random
import re
from datetime import datetime, timedelta
from collections import defaultdict

# File paths
INITIALIZE_SQL = '/home/bernard/projects_internal/cloud-architecture-workshop/globex/globex-store-db/contrib/sql/initialize.sql'

# Configuration
MIN_COMPLAINTS_PER_PRODUCT = 40
MAX_COMPLAINTS_PER_PRODUCT = 50
MAX_DATE = datetime(2026, 4, 1)

# Severity levels (evenly distributed)
SEVERITIES = ['critical', 'high', 'medium', 'low']

# Issue types (mostly defect)
ISSUE_TYPES = ['defect', 'defect', 'defect', 'defect', 'quality']

# Status options
STATUSES = ['open', 'open', 'open', 'in_progress']

# Resolution options
RESOLUTIONS = ['refund', 'replacement']

# Complaint templates by product category
COMPLAINT_TEMPLATES = {
    'clothing': {  # T-shirts, sweatshirts, polos, socks
        'critical': [
            "Severe allergic reaction to fabric within minutes of putting it on. Broke out in hives all over my torso and had to seek immediate medical attention.",
            "Toxic chemical smell that won't wash out even after multiple cycles. Makes me nauseous every time I open the closet where it's stored.",
            "Colors bleeding severely onto everything in the wash. Ruined an entire load of white laundry that is now permanently stained pink.",
            "Fabric completely disintegrated after first wash cycle. Found it in shreds at the bottom of the washing machine.",
            "Chemical burns on my skin from the fabric treatment. Had to visit urgent care for treatment of the blistering rash.",
            "Dye transferred onto my skin and won't come off. My torso is stained the color of the shirt and it's been three days of scrubbing.",
            "Material caused severe respiratory issues when wearing. I couldn't breathe properly and had to remove it immediately.",
            "Fabric ripped completely down the middle while I was wearing it in public. Extremely embarrassing and the tear happened with no strain.",
            "Entire garment fell apart in the washing machine on gentle cycle. Found it in multiple pieces, completely destroyed.",
            "Aggressive chemicals in the fabric caused skin blistering across my chest. My dermatologist confirmed it was a chemical reaction.",
            "Stitching failed catastrophically at all seams while wearing. The entire shirt literally fell apart on my body in public.",
            "Fabric discolored my undergarments permanently through chemical transfer. Everything I wore underneath is now ruined.",
            "Severe skin rash developed after wearing for just one hour. The itching and burning was unbearable and required medication.",
            "Item shrunk to half its original size in cold water wash. It would now fit a small child, completely unwearable.",
            "Thread count so poor the fabric is completely see-through. This is totally inappropriate to wear anywhere and not as advertised.",
        ],
        'high': [
            "Shrunk drastically in the wash despite following care instructions exactly. It's now three sizes smaller and completely unwearable.",
            "Color fading severely after just the first wash. It went from vibrant to completely washed out and looks years old.",
            "Seams started unraveling after just two wears during normal activity. It's now coming apart everywhere with threads hanging.",
            "Fabric pilling excessively after the very first wear. It looks like I've owned it for years, completely worn out already.",
            "Stitching ripped out completely at the shoulder seam. The entire product is falling apart and can't be worn.",
            "Neckline stretched out beyond recognition after wearing once. It now hangs down exposing my chest, completely ruined.",
            "Holes appearing in the fabric after minimal use and gentle washing. Very poor quality material that can't withstand normal wear.",
            "Material is incredibly itchy and uncomfortable against skin. I tried wearing it three times and can't tolerate the irritation.",
            "Hem came completely undone after the first wash. The bottom is now fraying badly and looks terrible.",
            "Graphic print cracked and peeled off entirely after one wash cycle. Now it just looks damaged and cheap with flaking pieces.",
            "Sleeves are two completely different lengths, obvious manufacturing defect. One is a full inch shorter than the other.",
            "Collar warped and won't lay flat no matter what I do. It sticks up awkwardly and looks terrible when worn.",
            "Fabric has a strange chemical odor that persists even after multiple washes. I've washed it five times and it still smells terrible.",
            "Significant color bleeding onto my skin when I wear it. I end up with colored marks all over my body after wearing.",
            "Material feels like sandpaper against skin. The texture is so rough it's extremely uncomfortable for any period of time.",
        ],
        'medium': [
            "Logo placement is completely off-center and crooked. It looks unprofessional and like a cheap knockoff product.",
            "Fabric feels significantly thinner than expected from the description. Not at all what was advertised in terms of quality.",
            "Fit is completely inconsistent with the published size chart. Appears they sent the wrong size entirely.",
            "Minor pilling on the fabric already visible. This is more than I would expect for a brand new item.",
            "Slight color variation between different parts of the garment. Poor quality control is evident in the manufacturing.",
            "Stitching quality is poor with visible flaws on the outside. You can see where the stitching is uneven and sloppy.",
            "Tag irritates my skin constantly and is very scratchy. This should really be a tagless design for comfort.",
            "Cuffs are already showing significant wear after just a few uses. The fabric is fraying at the edges.",
            "Print design is slightly misaligned and off-center. It's a noticeable quality issue that affects the appearance.",
            "Fabric stiffness won't soften even after multiple washings. It still feels rigid and uncomfortable to wear.",
            "Slight shrinkage noticed after washing per instructions. The fit is now tighter than when I first received it.",
            "Loose threads visible in multiple spots around the garment. Quality control should have caught these before shipping.",
            "Color is not as vibrant as shown in the product photos. It's noticeably duller and less appealing in person.",
            "Fabric wrinkles excessively and requires constant ironing. It looks rumpled within minutes of wearing.",
            "Seam allowance is visible on the outside at several points. This is poor construction and looks cheap.",
        ],
        'low': [
            "Tag is itchy and irritating against my neck. This should be a printed tag instead of a sewn-in fabric tag.",
            "Fabric weight feels lighter than my previous orders of this item. The quality seems to have decreased over time.",
            "Color is slightly different than what was shown in the product photos. It's close but not exactly as pictured.",
            "Hemline is slightly uneven around the bottom edge. It's a minor cosmetic issue but noticeable upon inspection.",
            "Small loose thread visible hanging from one of the seams. Minor quality issue that should have been trimmed.",
            "Fit runs slightly smaller than I expected based on sizing. Would have preferred if it was true to size.",
            "Material has a slight chemical smell upon opening the package. It mostly went away after washing though.",
            "Stitching color doesn't quite match the fabric color. It's close but you can see the difference in certain light.",
            "Packaging was wrinkled and the item arrived quite creased. Required ironing before I could wear it.",
            "Shade is slightly off from what I ordered based on the name. It's similar but not exactly the same tone.",
            "Fabric has minor texture inconsistencies in a few spots. Small areas feel different from the rest.",
            "Label placement could be better positioned for comfort. It's located where it rubs against my skin.",
        ],
    },
    'utensils': {  # Bottles, mugs, tumblers
        'critical': [
            "Bottle leaks from every seam and opening, completely unusable. Ruined my laptop, bag, and important documents with the spill.",
            "Lid broke off completely while I was drinking, sharp edges cut my hand badly. Required medical attention for the laceration.",
            "Vacuum seal catastrophically failed while carrying hot coffee. The contents spilled out and caused burns on my leg.",
            "Mug shattered into pieces when I filled it with hot liquid. Extremely dangerous and could have caused serious injury!",
            "Strong metallic taste contaminating all beverages, makes everything undrinkable. The flavor is so bad I can't use this at all.",
            "Bottle exploded in my car from pressure buildup. Hot coffee went everywhere and nearly caused me to have an accident.",
            "Lid flew off under normal pressure while drinking. Scalding liquid hit me directly in the face causing burns.",
            "Mug cracked during normal use and leaked boiling water onto my lap. I suffered minor burns and had to change clothes.",
            "Coating is flaking off into my drinks creating particles. This is a potential toxicity hazard and health concern.",
            "Handle snapped off completely while the container was full. Hot contents spilled directly onto my toddler nearby.",
            "Bottom of the bottle fell completely out while I was carrying it. Destroyed my laptop and several important documents.",
            "Seal failed completely causing a major spill during an important meeting. Embarrassing and damaged my notes and laptop.",
            "Sharp burr inside the rim cut my lip while drinking. I was bleeding and had to seek first aid.",
            "Thermal shock caused the glass to explode in my hand. Dangerous glass shards went everywhere in my kitchen.",
            "Rubber gasket disintegrated into my beverage in small pieces. This is a serious choking hazard for anyone drinking.",
        ],
        'high': [
            "Lid doesn't seal properly at all and leaks constantly from the threads. I can't take this anywhere without it dripping everywhere.",
            "Paint and coating actively peeling off into my beverages. This is a serious health hazard and makes it unsafe to use.",
            "Insulation has completely failed and doesn't keep beverages hot or cold. False advertising as it performs no better than a regular cup.",
            "Handle broke off after just normal daily use, not excessive force. Now the mug is extremely difficult to use safely.",
            "Bottle developed a crack after minimal use with proper care. The material quality is clearly very poor and substandard.",
            "Threads on the lid stripped immediately after a few uses. Now I can't properly close or seal the bottle at all.",
            "Leaks from every single opening and seam when tilted. The entire seal design appears to be defective.",
            "Interior coating is bubbling and peeling into my drinks. It's contaminating my beverages and potentially toxic.",
            "Straw mechanism broke completely on the second use. The seal won't hold and I can't drink from it anymore.",
            "Temperature control is non-existent, beverages cool in minutes. This is false advertising about the insulation properties.",
            "Mug developed a hairline crack around the base that slowly leaks. It's ruining the surfaces I set it on.",
            "Lid warped significantly from the dishwasher despite being labeled dishwasher safe. Now it doesn't fit properly at all.",
            "Flip-top mechanism jammed after a few uses then broke off completely. Can't open or close the bottle now.",
            "Vacuum seal was lost immediately after first use. There are no insulation properties at all anymore.",
            "Silicone seal degraded rapidly after just a few days. A slow leak developed that gets worse every day.",
        ],
        'medium': [
            "Extremely difficult to clean with mold forming in unreachable crevices. The design has areas that can't be accessed with a brush.",
            "Logo and branding wearing off after just a few hand washes. The printing quality is clearly very poor.",
            "Lid mechanism is very stiff and hard to operate with one hand. It requires two hands and significant force to open.",
            "Slight metallic taste that affects the flavor of all my beverages. It's noticeable and unpleasant every time I drink.",
            "Condensation constantly forming on the outside despite insulation claims. Leaves water rings on all surfaces.",
            "Opening is too narrow to properly clean the interior. I can't get a brush or sponge in there to clean effectively.",
            "Stains very easily despite manufacturer claiming it's stain-resistant. Coffee and tea leave permanent marks.",
            "Threading on the cap feels cheap and catches when screwing on. It doesn't thread smoothly and feels like it might strip.",
            "Design makes it tip over far too easily on flat surfaces. I've had multiple spills because it's top-heavy.",
            "Retains odors even after thorough washing with soap. Previous drinks affect the taste of new beverages.",
            "Exterior finish scratches very easily from normal handling. It looks old and worn after just a week of use.",
            "Actual capacity seems notably smaller than the advertised volume. It holds less than the stated amount.",
            "Insulation works but not nearly as long as claimed in specs. Drinks cool down much faster than advertised.",
            "Handle placement is awkward and uncomfortable to hold. The ergonomics are poor for carrying.",
            "Mouthpiece design is uncomfortable to drink from for extended periods. The angle and shape hurt my lips.",
        ],
        'low': [
            "Capacity is slightly smaller than what was advertised. It's close but not exactly the stated volume.",
            "Color is not exactly as shown in the product photo online. It's similar but a different shade than expected.",
            "Minor scratch visible on the surface right out of the package. Should have been caught by quality control.",
            "Lid is slightly loose but still functions adequately. It would be better if it fit more snugly.",
            "Finish has a minor imperfection on one side. It's cosmetic but noticeable when you look at it.",
            "Branding logo is slightly crooked and not perfectly centered. Minor quality control issue.",
            "Weight is heavier than I expected based on the description. Would prefer if it was a bit lighter.",
            "Opening diameter is smaller than I would prefer. Makes it harder to add ice cubes.",
            "Exterior has a small cosmetic blemish near the bottom. Doesn't affect function but is visible.",
            "Color shade is not quite as vibrant as shown in pictures. It's a bit duller than I expected.",
            "Lid requires more force to close than I would prefer. It takes significant pressure to seal.",
            "Minor manufacturing mark visible on the bottom surface. Small cosmetic flaw that shouldn't be there.",
        ],
    },
    'bags': {  # Backpacks, duffle bags, cooler bags
        'critical': [
            "Shoulder strap completely ripped off while carrying a normal load. This is a dangerous structural failure that could cause injury.",
            "Main zipper broke completely on the very first use. Now I cannot close or secure the bag at all.",
            "Material tore completely apart at the seams during normal use. Everything inside fell through onto the ground.",
            "Bottom of the bag gave way catastrophically and separated. I lost all contents onto a wet street, items damaged.",
            "Strap attachment point failed suddenly while I was carrying it. The bag fell and several expensive items inside were broken.",
            "Main compartment seam ripped completely open down the side. Total structural failure making the bag unusable.",
            "Handle tore completely off under minimal weight with sharp metal now exposed. This could easily cut someone badly.",
            "Fabric completely disintegrated when caught in light rain, not water resistant as advertised. The bag literally fell apart.",
            "Zipper teeth separated entirely from the fabric base. I cannot secure the bag anymore, zipper is completely destroyed.",
            "Shoulder strap snapped suddenly causing the bag to drop to the ground. The contents, including my laptop, were badly damaged.",
            "Base padding collapsed completely through the bottom. Items now fall through to the ground when I set it down.",
            "Carry handle ripped through the fabric creating a gaping hole. The bag is structurally unsound and unsafe to use.",
            "All three zippers failed simultaneously within the first week. This is clearly a manufacturing defect issue.",
            "Reinforced corners advertised as durable fell apart immediately. These were false quality claims in the marketing.",
            "Strap buckle shattered under normal adjustment with sharp metal fragments. The sharp pieces could seriously injure someone.",
        ],
        'high': [
            "Main zipper keeps separating even when fully closed. I cannot keep the bag securely closed at all.",
            "Strap stitching is visibly coming apart and unraveling. It's becoming unsafe to carry any significant weight.",
            "Water resistance failed completely in a light drizzle. All my contents got completely soaked despite the claims.",
            "Material is fraying badly after just minimal use and handling. The fabric quality is extremely poor.",
            "Velcro closures have completely lost their adhesion after just a few uses. They won't stay closed anymore.",
            "Interior lining is tearing away from the walls at multiple points. The bag is coming apart from the inside.",
            "Compression straps broke off at the attachment points. Now I cannot properly secure my load at all.",
            "Laptop compartment padding has disintegrated completely. There's no protection for electronics anymore.",
            "Side pockets have ripped at the seams and are unusable. They can't hold anything without items falling out.",
            "Rain cover attachment points all failed at once. The cover is now useless and can't attach to the bag.",
            "Zipper slider came completely off the track and won't go back. It's extremely difficult to zip anything now.",
            "Main carry handle stitching is rapidly unraveling at the base. It will completely detach very soon at this rate.",
            "All reflective strips are peeling off creating a hazard. They're hanging loose and could catch on things.",
            "Internal frame bent on the very first use under normal load. The bag won't hold its shape anymore.",
            "Mesh pockets have developed large tears throughout. Items constantly fall out through the holes.",
        ],
        'medium': [
            "Pockets are poorly designed and items fall out too easily. The depth and angle make them impractical to use.",
            "All zippers stick badly and are very difficult to operate. It takes significant force and multiple attempts.",
            "Fabric shows excessive wear marks after just light use. It looks like I've owned it for years already.",
            "Logo and branding peeling off after a very short time. The printing quality is obviously very poor.",
            "Stitching quality is inconsistent throughout the entire bag. Some seams look good, others are already failing.",
            "Straps constantly twist and won't stay adjusted where I set them. They slip back out of position constantly.",
            "Fabric pills excessively from normal friction and handling. It looks old and worn out already.",
            "Water bottle pocket is too shallow and bottles fall out. Poor design makes this feature nearly useless.",
            "Padding is insufficient for the level of protection advertised. Items inside are not well protected.",
            "Organization compartments are awkwardly sized for actual use. They don't fit standard items well.",
            "Zipper pulls feel cheap and are already bending out of shape. They'll likely break off soon.",
            "Shoulder pad slides around on the strap constantly. It won't stay positioned where it's useful.",
            "External compression straps are too short to be functional. They don't reach far enough to compress the load.",
            "Interior pockets are not reinforced and are sagging badly. They can't hold weight without drooping.",
            "Color is fading very noticeably after just limited use. It looks sun-bleached despite being new.",
        ],
        'low': [
            "Color is slightly different than what was advertised online. It's similar but not an exact match to photos.",
            "Minor loose thread hanging from one of the strap attachment points. Small quality control issue.",
            "Actual capacity feels smaller than I expected from the specs. It doesn't hold quite as much.",
            "Padding is slightly less substantial than I had hoped for. Would prefer more cushioning.",
            "Strap length adjustment mechanism is somewhat stiff. Takes more effort than expected to adjust.",
            "Fabric texture feels rougher than I anticipated. Not as soft or smooth as it appeared.",
            "External pocket placement is not ideal for my needs. Located in inconvenient spots.",
            "Branding and logos are larger than shown in the product photos. More prominent than I wanted.",
            "Zipper operation is louder than I expected it to be. Makes more noise than preferred.",
            "Weight distribution when loaded feels slightly off. Not as balanced as I hoped it would be.",
            "Interior color is darker than shown in the online photos. Different shade than expected.",
            "Handle grip could be more comfortable for extended carrying. Gets uncomfortable after a while.",
        ],
    },
    'office supplies': {  # Pens, webcam covers, journals, desk items
        'critical': [
            "Webcam cover adhesive was so aggressive it damaged my laptop screen coating when I tried to remove it. Left permanent marks on the screen.",
            "Pen leaked ink everywhere without warning, completely ruined important documents and my shirt. The mess was extensive and permanent.",
            "Stapler jammed violently and then broke apart leaving sharp metal pieces exposed. This poses a serious safety risk in the office.",
            "Product was completely non-functional right out of the package. Clearly defective from the factory with no quality control.",
            "Adhesive was so strong it literally ripped the paint off my laptop when removed. Caused significant damage to expensive equipment.",
            "Pen exploded in my shirt pocket during a client meeting. Created a permanent ink stain on expensive clothing.",
            "Journal spine cracked and broke immediately upon opening. All the pages scattered everywhere, completely destroyed.",
            "Internal mechanism spring shot out violently when I opened it. Nearly hit me in the eye, very dangerous.",
            "Ink cartridge burst inside the pen cap creating a massive mess. Got ink all over my hands, desk, and documents.",
            "Product off-gassed strong toxic fumes that made me feel ill. Had to remove it from my office due to the smell.",
            "Sharp unfinished edge on the product cut my hand deeply. Required bandaging and was bleeding quite a bit.",
            "Adhesive residue is completely impossible to remove from surface. It has permanently damaged my laptop with sticky marks.",
            "Pen tip broke off and became embedded in the paper I was writing on. Left a dangerous sharp piece of metal.",
            "Product sparked when I used it near my computer. There may be an electrical issue that could damage equipment.",
            "Overwhelming chemical smell caused headache and nausea within minutes. Had to air out my entire office space.",
        ],
        'high': [
            "Pen completely stopped working after just two days of light use. The ink flow stopped entirely despite being full.",
            "Adhesive failed immediately and won't stay attached to any surface. Completely defeats the purpose of the product.",
            "Journal binding fell completely apart after normal use. Pages are now falling out constantly and it's unusable.",
            "Primary mechanism broke on the very first use before I could even complete one task. Completely unusable product.",
            "Ink flow is extremely inconsistent, it skips every few words. Makes writing anything legible nearly impossible.",
            "Cover slider won't stay in the closed position at all. This completely defeats the purpose of having a privacy cover.",
            "Pages are tearing out at the binding after just one week. The journal is falling apart and unusable already.",
            "Clip broke off the pen immediately with no excessive force. Now I cannot attach it to anything.",
            "Adhesive left permanent sticky residue that's impossible to remove. It's all over my laptop and looks terrible.",
            "Product warped significantly from normal office temperature exposure. Now it doesn't fit or work properly.",
            "Elastic band snapped on the second time using it. Now there's no way to keep the journal closed.",
            "Button mechanism is completely jammed and won't operate. The product is stuck in one position permanently.",
            "Pen barrel cracked along the side after light use. Ink is slowly leaking out through the crack.",
            "Clasp mechanism failed and won't stay closed anymore. The journal opens randomly spilling papers everywhere.",
            "Paper quality is so poor that ink bleeds through every single page. Makes the back of each page unusable for writing.",
        ],
        'medium': [
            "Ink quality is very poor, it smears easily and skips constantly. Makes professional writing look sloppy and unprofessional.",
            "Pages in the journal are far too thin for fountain pen ink. Everything bleeds through to the other side rendering it useless.",
            "Overall product quality feels extremely cheap and flimsy. This is not at all as described in the marketing materials.",
            "Functionality is maddeningly inconsistent, it works sometimes but not others. Cannot rely on this for important tasks.",
            "Pen grip section is uncomfortable during any extended writing session. Causes hand fatigue and cramping quickly.",
            "Cover doesn't fit the device properly, there are visible gaps. Doesn't provide the coverage it's supposed to.",
            "Paper is not fountain pen friendly despite being advertised as such. All my good pens bleed and feather terribly.",
            "Eraser smudges the ink instead of removing it cleanly. Actually makes mistakes worse rather than fixing them.",
            "Binding is too tight and pages won't lay flat when open. Makes writing on pages very difficult and awkward.",
            "Ink dries out far too quickly when the pen is left uncapped. Even brief moments result in the tip drying completely.",
            "Mechanism operation requires excessive force to use. It shouldn't take this much effort for basic functionality.",
            "Product finish scratches extremely easily from normal office use. Looks old and worn after just a few days.",
            "Elastic closure is already stretching out noticeably. It will likely be useless soon at this rate.",
            "Pen writes far too light and thin making text hard to read. Have to press excessively hard to get visible lines.",
            "Adhesive strength is weakening quickly with each use. Soon it won't stick at all anymore.",
        ],
        'low': [
            "Color is not exactly as shown in the product photos. It's similar but a noticeably different shade.",
            "Product is slightly smaller than I expected from the description. The dimensions must be a bit off.",
            "Minor cosmetic defect visible on the surface of the product. Should have been caught in quality control.",
            "Build quality is acceptable but definitely not premium as advertised. Feels cheaper than the price suggests.",
            "Finish has a slight imperfection that's visible in good lighting. Minor manufacturing flaw.",
            "Size is marginally different than what was listed in specifications. Not exactly what I ordered.",
            "Ink color is slightly off from how it was described. Close but not quite the same shade.",
            "Paper shade is not quite as bright white as I expected. Has a slightly off-white tone to it.",
            "Logo placement is slightly off-center when you look closely. Minor alignment issue.",
            "Material feels somewhat cheaper than I had anticipated. Not quite the quality level expected.",
            "Packaging was poor quality but the actual product seems okay. Arrived somewhat damaged but functional.",
            "Weight is lighter than I would have preferred for this type of item. Feels a bit insubstantial.",
        ],
    },
    'fashion accessory': {  # Pins, earrings, keychains, face masks
        'critical': [
            "Pin clasp mechanism broke and the sharp point stabbed into my chest. Required medical attention for the puncture wound.",
            "Metal caused an immediate severe allergic reaction on my skin. Developed intense irritation and a spreading rash that required treatment.",
            "Earring post broke off completely leaving a dangerous sharp edge exposed. Could easily injure someone badly.",
            "Face mask elastic band snapped without warning and hit me in the face. Left a painful welt on my cheek.",
            "Pin back mechanism suddenly failed and poked a deep hole in my finger. Was quite painful and bled significantly.",
            "Metal oxidation caused my skin to turn green and the stain won't wash off. It's been several days of scrubbing with no improvement.",
            "Earring clasp sharp edge cut deeply into my earlobe while wearing. Had significant bleeding that required treatment to stop.",
            "Keychain split completely apart causing me to lose all my keys. This created a major security and inconvenience issue.",
            "Mask material caused severe breathing difficulty when wearing it. Felt like I was suffocating and had to remove it immediately.",
            "Pin pierced completely through my clothing into my skin underneath. Very painful injury that left a bleeding wound.",
            "Earring backing was far too tight and became embedded in my earlobe. Had to seek help to remove it safely.",
            "Chemical coating on the item caused a severe facial rash within hours. Dermatitis developed and required medication.",
            "Spring-loaded mechanism failed violently sending the pin jabbing into my hand. Created a painful puncture injury.",
            "Mask ear loops are so tight they cut deeply into the skin behind my ears. Caused painful lesions and raw areas.",
            "Metal component broke leaving a jagged sharp edge that cut my finger badly. Required bandaging for the bleeding.",
        ],
        'high': [
            "Primary clasp mechanism broke completely on the very first use. Now I cannot wear or use this item at all.",
            "Color faded dramatically after just the first wash or wearing. Looks completely washed out and old now.",
            "Material tarnished immediately upon first wearing, looks ancient and worn. This is obviously very poor quality metal.",
            "Elastic was far too weak and broke after just one single use. Now the item is completely unusable.",
            "Pin won't stay closed or secured, falls off constantly during wear. I've nearly lost it multiple times already.",
            "Earring post bent severely on first insertion attempt. Now it cannot be inserted into a piercing at all.",
            "Fabric pattern washed out completely after one laundering cycle. All the design and color is gone now.",
            "Chain link broke after wearing for only two days. The metal quality is obviously extremely poor.",
            "Coating is peeling off rapidly revealing cheap base metal underneath. Looks terrible and cheap now.",
            "Mask shrunk drastically after one wash despite following care instructions. It no longer fits at all.",
            "Clasp opens spontaneously during normal wear and I've lost the item twice. Cannot trust it to stay closed.",
            "Design element decoration fell off after minimal wear, adhesive completely failed. Now it looks plain and damaged.",
            "Metal discolored severely within just a few days of ownership. Looks tarnished and old already, very disappointing.",
            "Stitching is rapidly unraveling around all the edges. The item is visibly coming apart at the seams.",
            "Ring attachment broke off completely making it impossible to attach to anything. Defeats the entire purpose.",
        ],
        'medium': [
            "Logo and design are wearing off quickly with normal use. After just a week it's already noticeably faded.",
            "Size is significantly smaller than described in the product listing. It doesn't fit properly at all.",
            "Build quality is much lower than I expected for this price point. Feels cheap and poorly made.",
            "Finish is very uneven and inconsistent across the surface. Quality control was clearly lacking.",
            "Pin clutch backing is too loose and doesn't grip the post well. The pin slides around and won't stay in place.",
            "Material feels extremely flimsy and bends far too easily. Doesn't feel durable at all for regular use.",
            "Color is not nearly as vibrant as shown in product photos. Much duller and less appealing in person.",
            "Enamel coating already has several tiny chips appearing. Shows wear much faster than it should.",
            "Mask fabric is pilling badly after just a few wash cycles. Looks old and worn out already.",
            "Clasp is difficult to operate with just one hand. Requires two hands and significant dexterity.",
            "Finish is already showing noticeable wear marks from minimal handling. Surface scratches very easily.",
            "Material is noticeably thinner than I expected from the description. Feels insubstantial and cheap.",
            "Design looks slightly different in person than shown in images. Not quite what I thought I was ordering.",
            "Edges are not finished smoothly and have a rough uncomfortable feel. Poor attention to detail in manufacturing.",
            "Mask nose wire is inadequate and won't hold the shaped position. Keeps losing its form.",
        ],
        'low': [
            "Color is slightly different than shown in the product photo. Similar but not an exact match to what was displayed.",
            "Minor surface imperfection visible upon close inspection. Small manufacturing flaw that should have been caught.",
            "Weight is slightly lighter than I expected it would be. Feels a bit more insubstantial than anticipated.",
            "Finish has a small cosmetic blemish in one spot. Doesn't affect function but is noticeable.",
            "Size is marginally smaller than would be ideal for my use. Just slightly off from perfect.",
            "Packaging crushed or bent the item slightly during shipping. Minor cosmetic damage from poor packing.",
            "Clasp mechanism is a bit stiff initially when new. Takes some breaking in before it operates smoothly.",
            "Color tone is not quite as shown in the online photos. Close but perceptibly different shade.",
            "Minor scratch visible on the surface right out of packaging. Quality control should have caught this.",
            "Slightly less shiny and polished than it appeared in pictures. Finish is more matte than expected.",
            "Backing component feels cheap but still functions adequately. Would prefer higher quality materials.",
            "Proportions are slightly off from what the product image showed. Not exactly as pictured.",
        ],
    },
    'electronics': {  # Webcam lights, headphones
        'critical': [
            "Device actually caught fire while charging overnight on my desk. This is an extremely serious safety hazard that could have burned my house down!",
            "Received a significant electrical shock when plugging the device in. This is extremely dangerous and could cause serious injury or death.",
            "Battery exploded inside the device during normal use. This could have caused very serious injury or property damage.",
            "Product was completely dead on arrival and won't power on at all. Totally defective unit with zero functionality.",
            "Device overheated to the point of causing burns on my skin. The temperature reached dangerous levels during normal operation.",
            "Visible sparking from the charging port when I plugged it in. Immediate fire hazard that could ignite nearby materials.",
            "Battery swelled up significantly causing the device casing to crack open. Serious safety concern with potential for explosion.",
            "Short circuit inside the unit fried my laptop's USB port. Caused expensive damage to my other equipment.",
            "Smoke started coming from the device during regular use. Had to unplug it immediately and air out the room.",
            "Power cord frayed rapidly exposing live electrical wires inside. Creates a serious electrocution risk for anyone using it.",
            "Device is emitting a strong burning plastic smell during operation. This indicates serious internal problems and potential toxicity.",
            "Power surge when the device connected damaged multiple other electronics. Cost me hundreds in repairs to other equipment.",
            "Battery leaked corrosive chemical fluid inside the device. Potential toxic exposure and ruined the unit completely.",
            "Unit sparked violently and caused my computer to shut down unexpectedly. Lost important unsaved work due to this.",
            "Electrical overload caused my circuit breaker to trip repeatedly. This is a serious electrical hazard in my home.",
        ],
        'high': [
            "Device completely stopped working after just two uses with no warning. Total failure of core functionality.",
            "Sound quality is absolutely terrible with constant loud static and crackling. Makes it completely unusable for calls or music.",
            "Battery life is less than 10% of what was advertised in specs. This is blatant false advertising and misrepresentation.",
            "Charging port broke off after minimal use with normal care. Now there's no way to charge or power the device.",
            "Connection drops constantly every few minutes making it completely unreliable. Cannot use for any important tasks.",
            "One side is completely dead with no audio coming from the left ear. Only half the device works at all.",
            "Power button is stuck and I cannot turn the device on or off. The device is essentially bricked now.",
            "Bluetooth pairing fails every single time I try to connect. The wireless functionality simply does not work.",
            "Volume control is completely non-functional and stuck at maximum. Cannot adjust audio level at all which is painful.",
            "LED indicator lights all failed after just three uses. Now there's no way to see status or settings.",
            "Built-in microphone is completely non-functional, no input detected. Cannot use this for calls as advertised.",
            "Battery won't hold any charge at all, dies within minutes. Makes the device essentially tethered despite being wireless.",
            "Audio constantly cuts in and out making it completely unusable for calls. People can't understand what I'm saying.",
            "Device randomly shuts itself off during use without warning. Completely unreliable for any purpose.",
            "All control buttons are completely unresponsive to pressing. Cannot adjust any settings or functions at all.",
        ],
        'medium': [
            "Light brightness is much dimmer than advertised in specifications. Barely provides adequate illumination for video calls.",
            "Button mechanism is sticky and unreliable in operation. Requires multiple presses to register and feels cheap.",
            "Build quality feels extremely cheap and flimsy throughout. Does not match the quality suggested by the price point.",
            "Significant compatibility issues with common devices not mentioned anywhere in description. Doesn't work with my iPhone.",
            "Battery drains much faster than the specifications claimed. Gets maybe half the runtime that was advertised.",
            "Connection range is very limited, signal drops at short distances. Can barely move around while using it.",
            "Overall audio quality is mediocre at best with tinny sound. Lacks any bass and sounds hollow.",
            "Charging time is much longer than stated in product specs. Takes hours longer than advertised to fully charge.",
            "Plastic casing creaks and flexes feeling very fragile. Feels like it will break easily with normal handling.",
            "Status indicator lights are barely visible even in dim lighting. Cannot easily see what mode or status the device is in.",
            "Cable length is far too short for any practical use case. Should be at least twice as long to be useful.",
            "Ear padding is uncomfortable for any extended period of wearing. Causes pressure points and soreness quickly.",
            "Noticeable background hiss present at all volume levels. Distracting white noise that shouldn't be there.",
            "Touch controls are overly sensitive and trigger accidentally. Constantly pausing or skipping by accident.",
            "Auto-shutoff timer is far too aggressive and interrupts usage. Turns off in the middle of active use constantly.",
        ],
        'low': [
            "Color temperature of the light is different than shown in photos. Warmer tone than what was displayed online.",
            "Device is slightly bulkier than I expected from the images. Takes up more space than I anticipated.",
            "Minor cosmetic defect visible on the plastic housing. Small blemish that should have been caught in QC.",
            "Power indicator light is dimmer than I would prefer. Hard to see in bright ambient lighting.",
            "Finish has a small imperfection in one area. Doesn't affect function but is noticeable cosmetically.",
            "Cable is slightly stiffer than would be ideal. Could be more flexible for easier positioning.",
            "Button click sound is louder than I expected it to be. Makes an audible snap when pressed.",
            "Weight distribution feels slightly off when wearing. One side feels heavier than the other.",
            "Branding logo is more prominent than shown in photos. Larger and more visible than expected.",
            "Packaging seems excessive for such a small item. Wasteful amount of materials used.",
            "Included USB cable is shorter than I would have preferred. Would be more convenient if longer.",
            "Carrying case quality is subpar compared to device itself. Feels cheap and flimsy.",
        ],
    },
    'default': {  # For categories not specifically handled
        'critical': [
            "Product arrived completely defective and unusable from the very start. Zero functionality despite being brand new out of the box.",
            "Serious safety hazard as it broke in a dangerous way during normal use. Someone could easily be injured by this failure.",
            "Product failure caused significant damage to other property around it. This represents a major quality control failure.",
            "Severe quality issues make this product completely worthless. Cannot be used for its intended purpose at all.",
            "Product failed catastrophically during first use creating a hazardous situation. This is completely unacceptable for a new item.",
            "Manufacturing defect poses a serious and immediate safety risk. This should never have passed quality control inspection.",
            "Item arrived broken in a way that could easily cause injury to users. Sharp edges and broken parts are dangerous.",
            "Structural failure occurred during normal operation creating a dangerous situation. The product is fundamentally unsafe to use.",
            "Product released toxic-smelling fumes when used as directed. This is a serious health concern that makes it unusable.",
            "Critical component completely detached during normal use. Created a dangerous situation that could cause injury.",
            "Sharp edge was exposed after the product failed during use. Cut myself badly and required medical attention.",
            "Product collapsed completely under its normal rated load. This is a serious safety issue and design flaw.",
            "Internal mechanism failed violently during operation. Nearly caused injury and damaged nearby items.",
            "Chemical leak developed from inside the product during use. Potentially toxic substance was released.",
            "Identified significant fire risk during normal operation. Device became dangerously hot and is unsafe to use.",
        ],
        'high': [
            "Product broke after only minimal use with proper care. The materials used are clearly of very poor quality.",
            "Major manufacturing defect makes the product barely functional at all. Cannot perform its primary purpose reliably.",
            "Quality is far below my expectations and the product description claims. Feel misled by the advertising.",
            "Product completely stopped working after just two days of normal use. Total failure with no warning signs.",
            "Multiple components are failing simultaneously after brief use. Indicates systemic quality problems throughout.",
            "Product is completely unreliable and cannot be depended on. Fails frequently during normal operation.",
            "Structural integrity has been compromised making it unsafe to use. The product feels like it will break completely soon.",
            "Primary advertised function is completely non-operational. The main feature simply does not work at all.",
            "Material degradation happened rapidly within days of purchase. Product became unusable extremely quickly.",
            "Assembly fell completely apart during normal use without excessive force. Very poor construction quality overall.",
            "Finish is peeling off completely from the surface. Now it looks terrible and damaged after minimal use.",
            "Moving parts and mechanisms have seized up and won't operate. The product has completely failed mechanically.",
            "Product warped significantly from normal use conditions and environment. Now it doesn't fit or work properly.",
            "Main advertised feature doesn't work at all as described. This appears to be false advertising.",
            "Quality control was obviously severely lacking. Received a clearly defective unit that shouldn't have shipped.",
        ],
        'medium': [
            "Build quality is very inconsistent with multiple minor defects visible. Quality control is clearly inadequate.",
            "Functionality is not as described in the product listing at all. Different from what was advertised and expected.",
            "Materials used feel extremely cheap and low quality. Really not worth the price paid for this item.",
            "Performance falls well below the advertised specifications. Does not meet the claims made in marketing materials.",
            "Finish quality is poor with visible imperfections throughout. Surface is rough and uneven in many areas.",
            "Durability is highly questionable as it's already showing excessive wear. Doesn't seem like it will last long.",
            "Assembly was required but the instructions were unclear and confusing. Took much longer than it should have.",
            "Fit and finish are clearly substandard for this price point. Expected much better quality for what I paid.",
            "Product feels flimsy and lacks solid construction throughout. Seems like it will break easily with regular use.",
            "Several minor features are non-functional or missing entirely. Doesn't include everything that was advertised.",
            "Quality is inconsistent with the brand's reputation and past products. This item is noticeably worse than previous purchases.",
            "Materials used are noticeably cheaper than I expected. Different and lower quality than suggested by description.",
            "Workmanship appears sloppy with visible defects in multiple areas. Poor attention to detail in manufacturing.",
            "Operation is not nearly as smooth as described in reviews. Mechanism feels rough and catches frequently.",
            "Packaging is actually better quality than the product itself. Disappointed that more care went into the box than the item.",
        ],
        'low': [
            "Minor cosmetic defect visible on the surface that's acceptable but disappointing. Expected better quality control for a new item.",
            "Color and size are both slightly different than advertised online. Close but not exactly matching the product description.",
            "Build quality is adequate and functional but not particularly impressive. Expected slightly better for the price.",
            "Finish has a small blemish in one area that's noticeable. Minor manufacturing flaw that should have been caught.",
            "Product is slightly smaller than the description indicated. Dimensions appear to be a bit off from specifications.",
            "Color shade is not quite as shown in product photos. Similar tone but perceptibly different in person.",
            "Minor scratch is visible on the surface right out of packaging. Quality control should have caught this defect.",
            "Quality is acceptable for basic use but expected slightly better. Not bad but somewhat underwhelming overall.",
            "Packaging arrived somewhat damaged but the product seems okay. Poor packing job but item wasn't affected.",
            "Instructions could be significantly clearer and more detailed. Had some difficulty understanding the setup process.",
            "Minor difficulty during assembly that shouldn't have been an issue. Design could be more user-friendly.",
            "Appearance is slightly different from the photos shown online. Not drastically but noticeably different in some aspects.",
        ],
    },
    'drum sticks': {  # Drum sticks
        'critical': [
            "Stick splintered violently during normal playing sending sharp wood fragments into my eye. Required emergency medical attention for eye injury.",
            "Stick broke completely in half and the flying piece hit me directly in the face. Left a painful bruise and nearly caused serious eye injury.",
            "Wood treatment chemicals caused severe allergic reaction on my hands. Developed painful blisters and rash that required medical treatment.",
            "Stick shattered on first rimshot leaving extremely sharp jagged edges. Cut my hand badly on the splintered wood causing bleeding.",
            "Stick snapped during regular playing and the broken end stabbed into my palm. Puncture wound required stitches to close properly.",
            "Both sticks from the pair broke within minutes of each other during practice. Dangerous wood quality that could cause serious injury.",
            "Finish coating released toxic fumes when sticks were used extensively. Made me dizzy and nauseous from chemical exposure.",
            "Stick exploded into multiple sharp splinters on a normal stroke. Several fragments embedded in my hand requiring removal.",
            "Wood grain separated catastrophically causing stick to disintegrate mid-performance. Nearly injured myself with the flying debris.",
            "Tip broke off and flew directly into my bandmate's face during rehearsal. Could have caused a serious eye injury.",
            "Stick cracked and split lengthwise creating razor-sharp edges along the shaft. Sliced open my finger requiring medical attention.",
            "Defective wood caused stick to snap backwards hitting me in the throat. Extremely dangerous and painful impact.",
            "Both sticks warped severely and became dangerously unbalanced. One flew out of my hand and hit someone in the audience.",
            "Chemical preservative in the wood caused chemical burns on my palms. Had to seek medical treatment for the painful blistering.",
            "Stick fractured internally and collapsed during hard playing. The sudden failure caused me to strike myself in the face.",
        ],
        'high': [
            "Both sticks broke after less than one hour of normal playing. Completely unacceptable quality for professional use.",
            "Tips broke off both sticks after minimal use on standard drums. Wood quality is extremely poor and substandard.",
            "Sticks warped severely after just one practice session from normal playing. Now they're completely unbalanced and unusable.",
            "Wood grain is so poor that sticks feel like they'll break at any moment. Can't play with confidence using these.",
            "Finish started peeling off immediately leaving rough splinters. Causing blisters on my hands from the exposed wood.",
            "One stick is noticeably heavier than the other despite being a matched pair. Makes playing evenly completely impossible.",
            "Tips are chipping badly after just a few hours of use. Won't last anywhere near a normal stick's lifespan.",
            "Wood cracked along the grain on both sticks within first week. They're structurally compromised and unsafe to use.",
            "Sticks are severely unbalanced with weight distribution all wrong. Rebound is inconsistent making them unplayable.",
            "Finish is so slippery the sticks fly out of my hands constantly. Completely unsafe for any serious playing.",
            "Tips flattened and mushroomed after minimal cymbal work. Quality of wood is far too soft for drumming.",
            "Both sticks developed major cracks within days of light practice. Will definitely break completely very soon.",
            "Wood grain orientation is completely wrong causing weak points. Sticks bend visibly under normal playing pressure.",
            "Surface became rough and splintery after one session despite being sealed. Tearing up my hands during play.",
            "Sticks arrived already dried out and brittle. Cracking sounds with every hit indicating imminent catastrophic failure.",
        ],
        'medium': [
            "Weight of the two sticks is noticeably different despite labeled as matched pair. Affects playing balance significantly.",
            "Tips are poorly shaped and inconsistent between the two sticks. Sound quality is uneven between left and right hands.",
            "Finish is wearing off far too quickly from normal playing. After just a week they look like year-old sticks.",
            "Wood grain pattern indicates poor quality lumber was used. Visible weak points along the shaft are concerning.",
            "Sticks feel significantly lighter than the advertised weight specification. Not what I ordered for my playing style.",
            "Tips are showing excessive wear after just moderate playing time. Won't last nearly as long as quality sticks should.",
            "Balance point is off from standard placement making them awkward. Takes significant adjustment to play with these.",
            "Finish has a tacky feeling that's uncomfortable for extended playing. Hands stick to them in an unpleasant way.",
            "One stick has visible defects in the wood grain pattern. Concerned about durability and structural integrity.",
            "Diameter is inconsistent along the shaft on both sticks. You can feel the variations while playing.",
            "Tips are already showing minor chipping after light practice sessions. Quality is below what I expected.",
            "Wood feels somewhat soft and absorbs impact poorly. Rebound is not crisp and affects playing technique.",
            "Finish application is uneven with thick spots and thin spots. Aesthetically unappealing and affects grip.",
            "Sticks arrived somewhat dried out requiring immediate oiling. Should have been properly sealed at factory.",
            "Pitch and tone when striking is inconsistent between the pair. Indicates different wood densities used.",
        ],
        'low': [
            "Weight is slightly lighter than I prefer for my playing style. Would have ordered a different model if specs were accurate.",
            "Finish has minor cosmetic imperfections visible on close inspection. Doesn't affect play but looks somewhat cheap.",
            "Tips are shaped slightly differently from each other in the pair. Minor inconsistency but noticeable when playing.",
            "Wood grain pattern is less attractive than shown in product photos. More knots and irregularities than expected.",
            "Color of the wood is slightly different than pictured online. Not quite the shade I was expecting to receive.",
            "One stick has a small cosmetic blemish on the shaft. Doesn't impact function but is visible.",
            "Balance feels slightly different between the two sticks in the pair. Takes minor adjustment when switching hands.",
            "Finish is slightly less smooth than I expected from description. Not rough but not as polished as hoped.",
            "Tips are marginally smaller than my usual stick size. Close but not exactly what I'm used to playing with.",
            "Length appears slightly shorter than the stated specification. Difference is minor but measureable.",
            "Logo printing is slightly off-center on one stick. Small quality control issue that's purely cosmetic.",
            "Wood has minor surface irregularities that can be felt when gripping. Doesn't impact play significantly though.",
        ],
    },
    'drum shell sets': {  # Drum shell sets
        'critical': [
            "Lug completely ripped out of the shell during normal tuning causing shell to crack. Catastrophic structural failure making drum completely worthless.",
            "Mounting hardware failed causing the entire tom to fall during performance. Drum crashed down nearly hitting someone in the front row.",
            "Shell cracked completely around the entire circumference on first setup. Total structural failure indicating severe manufacturing defect.",
            "Tension rod threads stripped out of lug immediately under normal tension. Sharp metal edges exposed that cut my hand badly.",
            "Bass drum hoop split apart violently when tensioning the head. Flying metal piece nearly hit me in the face causing injury.",
            "Bearing edge has extremely sharp burrs that cut my hands while installing heads. Required medical attention for the deep cuts.",
            "Shell delaminated catastrophically with plies separating completely. Drum literally fell apart into layers during playing.",
            "Floor tom leg bracket ripped completely out of shell under normal weight. Drum collapsed causing damage to other equipment.",
            "Snare strainer mechanism broke off taking chunk of shell with it. Left gaping hole in the drum making it completely unusable.",
            "Vent grommet had razor-sharp edges that severely cut my finger during head installation. Bled significantly and needed stitches.",
            "All lugs are misaligned causing uneven tension that cracked the shell. Structural damage makes the drum dangerous to use.",
            "Mounting bracket failed completely during transport and drum fell onto concrete. Hardware defect led to expensive damage.",
            "Shell finish released toxic fumes when drums were played in enclosed space. Made entire band sick from chemical exposure.",
            "Hoop warped so severely it couldn't mount on shell without extreme force. Forcing it caused shell to crack completely through.",
            "Bass drum spur pierced through shell due to weak mounting point. Dangerous hardware failure during performance.",
        ],
        'high': [
            "All tension rods stripped out after just one tuning session. Now impossible to properly tune any of the drums.",
            "Shell is severely warped and won't hold round shape under tension. Cannot get even tuning anywhere on the drum head.",
            "Finish is peeling off in large sheets after minimal use and handling. Drums look terrible and damaged after just one week.",
            "Lugs are loosening constantly requiring re-tightening after every song. Hardware quality is completely inadequate for gigging.",
            "Bearing edges are so rough they're tearing drum heads during installation. Already destroyed two expensive heads trying to mount them.",
            "Tom mount is stripping out and won't hold toms in position anymore. Everything sags and moves during playing.",
            "Hoops are severely out of round making even tensioning impossible. Drums sound terrible no matter how I try to tune them.",
            "All chrome hardware is rusting despite being stored properly indoors. Finish quality is obviously very poor and substandard.",
            "Shell has visible voids and gaps in the plies internally. Structural integrity is compromised and affects sound quality severely.",
            "Snare wires broke after just two practice sessions from normal playing. Metal quality is far below acceptable standards.",
            "Resonant head seat is damaged allowing head to slip during playing. Cannot maintain consistent sound or tuning.",
            "Bass drum spurs won't lock in position and collapse during playing. Drum slides around stage constantly.",
            "Mounting hardware threads are already stripping from normal assembly. Will be completely unusable very soon at this rate.",
            "Internal reinforcement rings are separating from shells. Can hear rattling and feel structural weakness developing.",
            "All lugs are bent and misaligned from factory making tuning extremely difficult. Quality control was clearly non-existent.",
        ],
        'medium': [
            "Bearing edges are inconsistent and uneven around the circumference. Makes getting good sound and tuning very difficult.",
            "Finish has multiple small imperfections and rough spots throughout. Doesn't look professional quality for the price paid.",
            "Some lugs feel loose even when fully tightened on shell. Concerned about long-term stability and reliability.",
            "Internal finish is very rough with visible splinters and unfinished wood. Not what I expected from this price point.",
            "Drum depths are slightly inconsistent between toms in the set. Throws off the visual and tonal progression.",
            "Vent grommets are poorly installed and not flush with shell. Looks sloppy and detracts from overall appearance.",
            "Hoops have minor dings and imperfections affecting head seating. Getting even tension is more difficult than it should be.",
            "Hardware feels cheap and lightweight compared to other kits. Doesn't inspire confidence in long-term durability.",
            "Shell seam is visible and rough on one of the drums. Finish doesn't fully cover the manufacturing joint.",
            "Mounting brackets feel flimsy and flex under the weight of toms. Not as stable as they should be for this price.",
            "Badge is crooked and not centered on bass drum. Looks unprofessional and suggests poor quality control.",
            "Some tension rod threads feel rough and catch when tuning. Concerned they may strip with regular use.",
            "Interior shell finish is inconsistent with drips and rough patches. Sloppy workmanship evident throughout.",
            "Snare bed is cut too deep affecting snare wire contact. Takes excessive tension to get proper snare response.",
            "Floor tom legs are slightly different lengths making setup uneven. Had to shim to get drum level.",
        ],
        'low': [
            "Finish color is slightly different from what was shown in photos. Similar but not exactly the same shade throughout.",
            "One small cosmetic imperfection in the wrap finish visible. Minor bubble or scratch from manufacturing process.",
            "Lugs are not perfectly aligned visually though they function fine. Small aesthetic issue that bugs me.",
            "Bearing edge has one small flat spot that's barely noticeable. Doesn't significantly affect sound but I can tell it's there.",
            "Badge logo is slightly crooked on one of the toms. Purely cosmetic but wish it was perfectly straight.",
            "One tension rod is slightly harder to turn than the others. Still works but requires more effort to tune.",
            "Drum depths are marginally different than specifications listed. Very close but not exactly as advertised.",
            "Internal reinforcement rings are slightly visible through vent holes. Minor aesthetic concern that doesn't affect sound.",
            "Chrome finish has very minor clouding in one small area. Hardly noticeable unless looking closely.",
            "One hoop has a barely perceptible wobble when rolled on flat surface. Doesn't affect function on the drum.",
            "Vent grommet is slightly off-center on one drum. Purely visual issue that doesn't impact performance.",
            "Packaging could have been better with more protection around hardware. Items arrived fine but seemed risky.",
        ],
    },
}

def extract_products():
    """Extract all products from catalog with their categories"""
    products = {}

    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    # Extract category names
    categories = {}
    cat_pattern = r"INSERT INTO category \(category_id, category\) VALUES \((\d+), '([^']+)'\);"
    for match in re.finditer(cat_pattern, content):
        cat_id, cat_name = match.groups()
        categories[cat_id] = cat_name

    # Extract products
    prod_pattern = r"INSERT INTO catalog \(item_id, name, description, category, price\) VALUES \('([^']+)', '([^']+)', '[^']*', (\d+), ([\d.]+)\);"
    for match in re.finditer(prod_pattern, content):
        item_id, name, category_id, price = match.groups()
        products[item_id] = {
            'name': name,
            'category': categories.get(category_id, 'default'),
            'price': float(price)
        }

    return products

def extract_orders_by_product():
    """Extract all orders for each product with timestamps"""
    orders_by_product = defaultdict(list)

    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    # Get all line items (product -> order mappings)
    line_item_pattern = r"INSERT INTO public\.line_item \([^)]+\) VALUES \(\d+, [\d.]+, '([^']+)', \d+, (\d+)\);"
    product_orders = defaultdict(set)

    for match in re.finditer(line_item_pattern, content):
        product_code, order_id = match.groups()
        product_orders[product_code].add(order_id)

    # Get order details (customer_id and timestamp)
    order_pattern = r"INSERT INTO public\.orders \(id, customer_id, order_ts\) VALUES \((\d+), '([^']+)', '([^']+)'\);"
    order_details = {}

    for match in re.finditer(order_pattern, content):
        order_id, customer_id, order_ts = match.groups()
        # Handle both timestamp formats (with and without fractional seconds)
        try:
            parsed_ts = datetime.strptime(order_ts, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            parsed_ts = datetime.strptime(order_ts, '%Y-%m-%d %H:%M:%S')

        order_details[order_id] = {
            'customer_id': customer_id,
            'order_ts': parsed_ts
        }

    # Combine: for each product, get list of orders with full details
    for product_code, order_ids in product_orders.items():
        for order_id in order_ids:
            if order_id in order_details:
                orders_by_product[product_code].append({
                    'order_id': int(order_id),
                    'customer_id': order_details[order_id]['customer_id'],
                    'order_ts': order_details[order_id]['order_ts']
                })

    return orders_by_product

def find_max_complaint_id():
    """Find the maximum complaint ID in the database"""
    with open(INITIALIZE_SQL, 'r') as f:
        content = f.read()

    complaint_ids = []
    pattern = r"INSERT INTO public\.complaints \(id,[^)]+\) VALUES \((\d+),"

    for match in re.finditer(pattern, content):
        complaint_ids.append(int(match.group(1)))

    return max(complaint_ids) if complaint_ids else 0

def generate_complaint_timestamp(order_ts):
    """Generate a complaint timestamp after the order date but before MAX_DATE"""
    # Complaint should be between order date and MAX_DATE
    # Typically 1-60 days after order
    days_after_order = random.randint(1, 60)
    complaint_ts = order_ts + timedelta(days=days_after_order)

    # Ensure it doesn't exceed MAX_DATE
    if complaint_ts > MAX_DATE:
        seconds_diff = (MAX_DATE - order_ts).total_seconds()
        if seconds_diff > 0:
            random_seconds = random.random() * seconds_diff
            complaint_ts = order_ts + timedelta(seconds=random_seconds)
        else:
            complaint_ts = order_ts + timedelta(hours=random.randint(1, 24))

    return complaint_ts.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def get_complaint_templates(category):
    """Get complaint templates for a product category"""
    # Map category to templates
    if category in COMPLAINT_TEMPLATES:
        return COMPLAINT_TEMPLATES[category]
    else:
        return COMPLAINT_TEMPLATES['default']

def generate_complaints_for_all_products(products, orders_by_product):
    """Generate complaints for all products"""

    start_id = find_max_complaint_id() + 1
    complaint_id = start_id

    all_complaints = []
    stats = {
        'total': 0,
        'by_severity': defaultdict(int),
        'by_issue_type': defaultdict(int),
        'products_processed': 0,
        'products_skipped': 0,
    }

    # Track used order+product combinations to avoid duplicates
    used_combinations = set()

    for product_code, product_info in sorted(products.items()):
        # Check if we have orders for this product
        if product_code not in orders_by_product:
            print(f"# Warning: No orders found for product {product_code} ({product_info['name']})", file=sys.stderr)
            stats['products_skipped'] += 1
            continue

        available_orders = orders_by_product[product_code]

        # Determine number of complaints for this product
        num_complaints = random.randint(MIN_COMPLAINTS_PER_PRODUCT, MAX_COMPLAINTS_PER_PRODUCT)

        # Can't have more complaints than orders
        if len(available_orders) < num_complaints:
            print(f"# Warning: Product {product_code} only has {len(available_orders)} orders, generating that many complaints", file=sys.stderr)
            num_complaints = len(available_orders)

        if num_complaints == 0:
            stats['products_skipped'] += 1
            continue

        # Select random orders for complaints (no duplicates)
        selected_orders = random.sample(available_orders, num_complaints)

        # Get complaint templates for this category
        templates = get_complaint_templates(product_info['category'])

        # Distribute severities evenly
        severities = []
        for _ in range(num_complaints // len(SEVERITIES)):
            severities.extend(SEVERITIES)
        remaining = num_complaints - len(severities)
        severities.extend(random.sample(SEVERITIES, remaining))
        random.shuffle(severities)

        # Generate complaints for this product
        for i, order in enumerate(selected_orders):
            severity = severities[i]
            issue_type = random.choice(ISSUE_TYPES)
            resolution = random.choice(RESOLUTIONS)
            status = random.choice(STATUSES)

            # Select a complaint description for this severity
            complaint_text = random.choice(templates[severity])

            # Escape single quotes
            complaint_text = complaint_text.replace("'", "''")

            # Generate timestamps
            created_at = generate_complaint_timestamp(order['order_ts'])
            updated_at = created_at

            sql = (
                f"INSERT INTO public.complaints (id, user_id, order_id, product_code, issue_type, severity, "
                f"complaint, status, resolution, created_at, updated_at, version) VALUES "
                f"({complaint_id}, '{order['customer_id']}', {order['order_id']}, '{product_code}', "
                f"'{issue_type}', '{severity}', '{complaint_text}', '{status}', '{resolution}', "
                f"'{created_at}', '{updated_at}', 1);"
            )

            all_complaints.append(sql)

            # Track stats
            stats['total'] += 1
            stats['by_severity'][severity] += 1
            stats['by_issue_type'][issue_type] += 1

            # Mark combination as used
            used_combinations.add((product_code, order['order_id']))

            complaint_id += 1

        stats['products_processed'] += 1

    return all_complaints, stats

def main():
    import sys

    print("-- Generated complaints for all products", file=sys.stderr)
    print("-- Extracting products from catalog...", file=sys.stderr)

    # Extract data
    products = extract_products()
    print(f"-- Found {len(products)} products", file=sys.stderr)

    print("-- Extracting orders by product...", file=sys.stderr)
    orders_by_product = extract_orders_by_product()
    print(f"-- Found orders for {len(orders_by_product)} products", file=sys.stderr)

    # Set random seed for reproducibility
    random.seed(42)

    # Generate complaints
    print(f"-- Generating {MIN_COMPLAINTS_PER_PRODUCT}-{MAX_COMPLAINTS_PER_PRODUCT} complaints per product...", file=sys.stderr)
    complaints, stats = generate_complaints_for_all_products(products, orders_by_product)

    # Print statistics
    print(f"-- Generated {stats['total']} total complaints", file=sys.stderr)
    print(f"-- Products processed: {stats['products_processed']}", file=sys.stderr)
    print(f"-- Products skipped (no orders): {stats['products_skipped']}", file=sys.stderr)
    print("-- Severity distribution:", file=sys.stderr)
    for severity in SEVERITIES:
        print(f"--   {severity}: {stats['by_severity'][severity]}", file=sys.stderr)
    print("-- Issue type distribution:", file=sys.stderr)
    for issue_type in ['defect', 'quality']:
        print(f"--   {issue_type}: {stats['by_issue_type'][issue_type]}", file=sys.stderr)

    # Output SQL
    print()
    print("-- Complaints for all products in catalog")
    for sql in complaints:
        print(sql)

if __name__ == '__main__':
    import sys
    main()
