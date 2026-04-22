import random

GHOST_CLUES = {

    ('happiness', 5): [
        ("Happiness", "I almost forgot what warmth felt like.",
         "A faint smile, maybe once or twice.\nLike catching the scent of something good\n"
         "from a room you can no longer enter.\n\nIt was barely there.\nBut I felt it. Briefly."),
        ("Happiness", "There was a moment — just one — that I held onto.",
         "I don't remember what caused it.\nOnly that for a second, something lifted.\n\n"
         "I kept reaching for it afterwards.\nIt never came back quite the same."),
        ("Happiness", "Joy was a stranger who knocked once and left.",
         "I heard it at the door. I even opened it.\n\n"
         "But by the time I looked outside,\nthere was nothing there."),
        ("Happiness", "I think I smiled, somewhere in those years.",
         "I can't be certain.\nThe memory is blurred at the edges,\n"
         "like a photograph left in the sun too long.\n\nBut I believe it happened."),
        ("Happiness", "A small warmth. Fleeting. Unannounced.",
         "The kind that doesn't announce itself.\nIt was just there, briefly,\n"
         "between two ordinary moments.\n\nAnd then it wasn't."),
        ("Happiness", "Once, something made me laugh.",
         "I don't remember what it was.\nOnly the feeling — sudden and bright,\n"
         "like a candle lit in a draught.\n\nGone before I could cup my hands around it."),
        ("Happiness", "Warmth visited. It did not stay long.",
         "I noticed it the way you notice good weather —\nonly in hindsight,\nwhen the cold has returned.\n\n"
         "I should have paid more attention."),
        ("Happiness", "A trace of something sweet. That is all.",
         "Like the last note of a song\nyou heard through a closing door.\n\n"
         "Present. Then absent.\nI am not sure it counted."),
        ("Happiness", "Happiness was a rumour I occasionally believed.",
         "Some days, the evidence seemed real.\nA kind word. A quiet morning.\n\n"
         "But I never quite trusted it\nenough to let it settle."),
        ("Happiness", "I felt it the way you feel sunshine through glass.",
         "Present, yes.\nBut not quite reaching you.\nNot quite enough to call it warmth.\n\n"
         "Close, though. Almost."),
    ],

    ('happiness', 10): [
        ("Happiness", "There were good moments. I kept them close.",
         "A laugh shared with someone.\nA quiet afternoon that felt just right.\n"
         "Not many — but enough to remember.\n\nJoy visited me, even if it didn't stay long."),
        ("Happiness", "Some days were genuinely good.",
         "Not perfect. Not many. But real.\n\n"
         "I remember a particular Tuesday —\nthe light was right, and so was everything else."),
        ("Happiness", "I found small joys and hoarded them like coins.",
         "A cup of tea at the right temperature.\nThe sound of rain on a roof I liked.\n\n"
         "Nothing grand. But mine."),
        ("Happiness", "There was enough happiness to be grateful for.",
         "Not a flood — a steady drip.\nEnough to keep the ground from drying out.\n\n"
         "I am not complaining.\nI was luckier than some."),
        ("Happiness", "Joy came and went on its own schedule.",
         "I learned not to chase it.\nSometimes it found me on a bench in the park,\n"
         "or midway through an ordinary sentence.\n\nI appreciated it when it did."),
        ("Happiness", "I had my moments of brightness.",
         "They weren't rare enough to be precious\nor common enough to be taken for granted.\n\n"
         "They were just — present.\nA mild, reasonable amount of light."),
        ("Happiness", "Enough warmth to get through the cold parts.",
         "There were cold parts.\nBut I had enough stored up\nto last me through most of them.\n\n"
         "That is not nothing."),
        ("Happiness", "Some mornings I woke up genuinely glad.",
         "Not every morning. But enough of them.\nThe kind of glad that comes before coffee, before thought.\n\n"
         "Just: glad."),
        ("Happiness", "I knew contentment, if not quite joy.",
         "Content is underrated.\nI sat in it often —\nthe quiet satisfaction of a day that simply went fine.\n\n"
         "I wish I had valued it more."),
        ("Happiness", "Laughter was a regular visitor.",
         "Not raucous. Not constant. But it came.\nOver small things, mostly.\n\n"
         "I think that is the best kind —\nthe laughter that costs nothing\nand means everything."),
    ],

    ('happiness', 20): [
        ("Happiness", "Most days had something worth smiling about.",
         "Warm meals. Kind words. Small victories.\nI was content more often than I admitted.\n"
         "Life handed me enough brightness\n\nto fill the room, if I let it."),
        ("Happiness", "I was, more often than not, genuinely happy.",
         "Not performing it. Not pretending.\nActually, quietly, reliably happy.\n\n"
         "I did not always know how rare that was."),
        ("Happiness", "Joy was a familiar presence in my life.",
         "It lived in the usual places —\nthe kitchen, the garden,\nthe faces of people I loved.\n\n"
         "I did not have to search very hard for it."),
        ("Happiness", "I laughed often and meant it.",
         "Genuinely, from the chest.\nThe kind that leaves you breathless and slightly undignified.\n\n"
         "I would give a great deal\nto laugh like that once more."),
        ("Happiness", "There was real warmth in my days.",
         "Not the borrowed kind.\nNot the kind you manufacture to get through a difficult month.\n\n"
         "The real thing. Reliable. Mine."),
        ("Happiness", "Happiness was familiar territory.",
         "I knew its geography well —\nwhere to find it, how long it would last, what to bring.\n\n"
         "I visited often."),
        ("Happiness", "The good outweighed the difficult, most years.",
         "That is not a small thing to say.\nMost years, the scale tipped\ntoward something worth having.\n\n"
         "I should have said so out loud more often."),
        ("Happiness", "I was surrounded by things I loved.",
         "People, places, small rituals.\nThey accumulated, quietly,\ninto a life that was genuinely mine.\n\n"
         "That is more than most get."),
        ("Happiness", "On balance, my life was full of light.",
         "Not without shadow. But on balance — light.\nThe kind that makes everything\nlook a little warmer than it is.\n\n"
         "I am glad I lived in it."),
        ("Happiness", "I was happy enough that I almost forgot to notice.",
         "That is the thing about steady happiness —\nyou stop counting it. You just live in it.\n\n"
         "I forgot to be grateful.\nI regret that now."),
    ],

    ('happiness', 30): [
        ("Happiness", "I was so full of joy it frightened me sometimes.",
         "Every sunrise felt like a personal gift.\nI laughed loudly and loved freely.\n"
         "My heart could have burst from it all.\n\nI miss that version of myself terribly."),
        ("Happiness", "Joy was the loudest thing about me.",
         "It spilled out of me without warning.\nInto rooms. Into conversations.\nInto people who were not always ready for it.\n\n"
         "I could not help it. I was full."),
        ("Happiness", "I loved being alive. Every single day.",
         "Not in a quiet way.\nIn a way that made other people slightly tired.\n\n"
         "I do not apologise for it.\nIt was real."),
        ("Happiness", "Happiness was not something I felt — it was something I was.",
         "It had become inseparable from me.\nFrom the way I walked, the way I spoke,\nthe way I entered a room.\n\n"
         "I did not know who I was without it."),
        ("Happiness", "I collected joy the way others collect worries.",
         "Obsessively. Gratefully. Constantly.\nI could find it anywhere.\n\n"
         "The world was generous to me,\nand I knew it."),
        ("Happiness", "My heart was unreasonably, embarrassingly full.",
         "People asked how I managed it.\nI never had a good answer.\n\n"
         "It was simply how I was made.\nOr how I chose to be.\nI am no longer certain which."),
        ("Happiness", "I lived as though joy were infinite.",
         "Perhaps it was.\nPerhaps that was the secret —\nnot that I had more,\nbut that I spent it freely\nand it kept returning."),
        ("Happiness", "The world delighted me. Constantly. Helplessly.",
         "Light through leaves.\nThe smell before rain.\nA good sentence in a book I loved.\n\n"
         "Everything was a gift.\nI received it all."),
        ("Happiness", "I was loved and I knew it and I let it matter.",
         "I did not hold it at arm's length.\nI let it in.\n\n"
         "That took courage, in the end.\nI am proud of that."),
        ("Happiness", "I had so much joy it sometimes felt unfair.",
         "I wondered if I was using up someone else's share.\n\n"
         "I decided to be grateful anyway.\nTo spend it well.\nTo make sure it reached others.\nI hope it did."),
    ],

    ('sadness', 5): [
        ("Sadness", "Just a small heaviness. Nothing dramatic.",
         "Like wearing a damp coat you forget to remove.\nA faint ache in a place with no name.\n"
         "I didn't cry. I didn't need to.\n\nIt was simply... there."),
        ("Sadness", "A low hum of something not quite right.",
         "Not grief. Not even unhappiness.\nJust a faint dissonance,\nlike a note slightly out of tune.\n\n"
         "I learned to live alongside it."),
        ("Sadness", "Some things left a small mark.",
         "Not deep. Not lasting.\nJust enough to remind me that I had felt something.\n\n"
         "That is not the worst thing."),
        ("Sadness", "A shadow at the edge of most good days.",
         "Barely noticeable.\nOnly visible when the light was just right.\n\n"
         "I stopped looking for it.\nThat helped."),
        ("Sadness", "The sadness was quiet. It kept its distance.",
         "It did not interfere much.\nJust sat in a corner of the room and watched.\n\n"
         "I got used to it."),
        ("Sadness", "A small melancholy, nothing more.",
         "The kind that makes autumn feel appropriate.\nThat makes slow music make sense.\n\n"
         "Manageable. Even useful, sometimes.\nIt kept me honest."),
        ("Sadness", "Some losses were small but they were still losses.",
         "I do not want to overstate it. They were small.\n\n"
         "But I noticed them.\nAnd sometimes, in quiet moments, I still do."),
        ("Sadness", "A mild sadness, like a sky that cannot quite decide.",
         "Not raining. Not sunny.\nJust grey in a way that is not unpleasant, only... grey.\n\n"
         "I lived under that sky often."),
        ("Sadness", "I missed things. Occasionally. Briefly.",
         "People who left.\nVersions of myself I had grown out of.\n\n"
         "The missing was soft. Bearable.\nI carried it without much trouble."),
        ("Sadness", "There was a gentle wistfulness to my days.",
         "Nothing sharp.\nJust the occasional sense\nthat something fine had passed\nbefore I had fully appreciated it.\n\n"
         "I did my best."),
    ],

    ('sadness', 10): [
        ("Sadness", "Some things didn't turn out the way I hoped.",
         "I kept it quiet — tucked behind a polite smile.\nThe kind of sadness that doesn't make a scene.\n"
         "It just follows you home\n\nand sits at the table without being invited."),
        ("Sadness", "There were losses I did not speak about.",
         "Not because they were shameful.\nBut because I was not sure anyone would understand.\n\n"
         "So I carried them alone.\nThey were heavier than I expected."),
        ("Sadness", "Certain days were harder than I let on.",
         "I had a very good face for it —\nthe face that says: I am fine.\n\n"
         "I was, mostly.\nBut not always. And not entirely."),
        ("Sadness", "I grieved things quietly, in private.",
         "The way you grieve something\nyou are not sure you were supposed to love that much.\n\n"
         "Carefully. Thoroughly. Alone."),
        ("Sadness", "Some chapters ended before I was ready.",
         "I turned the pages anyway.\nBut I lingered on the last ones.\n\n"
         "Read them again when no one was watching."),
        ("Sadness", "A recurring ache. Manageable, but present.",
         "The kind that does not stop you\nbut slows you slightly.\n\n"
         "Like walking with a stone in your shoe\nyou never quite stop to remove."),
        ("Sadness", "I was sad more often than I admitted.",
         "Not devastatingly.\nNot in ways that showed.\nBut underneath, regularly, in the evenings.\n\n"
         "I got used to it. That is its own kind of sadness."),
        ("Sadness", "Disappointment visited me often enough to feel familiar.",
         "I stopped being surprised by it.\nThat was practical.\n\n"
         "Whether it was wise, I am less certain."),
        ("Sadness", "I missed people who were still alive.",
         "That particular kind of grief.\nWhen someone is still there\nbut the version of them you loved has changed.\n\n"
         "You cannot mourn it properly. So you don't."),
        ("Sadness", "The sadness was real, even if it was small.",
         "I do not want to exaggerate.\nBut I do not want to dismiss it either.\n\n"
         "It was there.\nIt meant something.\nI felt it honestly."),
    ],

    ('sadness', 20): [
        ("Sadness", "The tears came more often than I'd like to admit.",
         "Something was always missing.\nI couldn't name it, but I felt its absence\n"
         "in every quiet room and long evening.\n\nGrief has many shapes. Mine was formless."),
        ("Sadness", "Loss became a kind of companion.",
         "I did not choose it.\nBut after a certain point, it was simply always there.\n\n"
         "I learned to walk beside it\nwithout letting it lead."),
        ("Sadness", "I cried more than most people knew.",
         "In the car. In the shower.\nIn the in-between moments when no one was looking.\n\n"
         "I was not ashamed.\nBut I was tired."),
        ("Sadness", "There were years that felt like extended grief.",
         "Not for one thing.\nFor everything, slightly.\nA low-level mourning\nthat coloured everything I touched.\n\n"
         "I kept going. But it cost something."),
        ("Sadness", "The sadness was substantive. It had weight.",
         "I felt it in my chest.\nIn the way the morning looked.\n\n"
         "It was not nothing."),
        ("Sadness", "I carried grief for things I never said out loud.",
         "Regrets shaped like silences.\nApologies I rehearsed but never delivered.\n\n"
         "They accumulated.\nI feel them still."),
        ("Sadness", "Melancholy was my default setting for many years.",
         "Not depression. Not despair.\nJust a persistent low note underneath everything.\n\n"
         "Like an instrument slightly out of tune\nplaying in a room you cannot leave."),
        ("Sadness", "I mourned things before I had even lost them.",
         "The anticipatory grief\nof someone who loves too much\nand knows too well how things end.\n\n"
         "It exhausted me. It also meant I paid attention."),
        ("Sadness", "Some pain did not go away. I learned to live around it.",
         "Not through it. Not past it. Around it.\n\n"
         "Like rerouting a river.\nYou don't remove the obstacle.\nYou just find another way."),
        ("Sadness", "The sadness shaped me. I cannot pretend it didn't.",
         "Everything I made, I made in its shadow.\nEverything I loved, I loved harder\nbecause of how much I had already lost.\n\n"
         "It was not a gift. But it was not wasted."),
    ],

    ('sadness', 30): [
        ("Sadness", "I wept. Deeply. For a very long time.",
         "The sorrow became as natural as breathing.\nI stopped fighting it and let it stay.\n"
         "It hollowed me out, slowly,\n\nuntil there was more emptiness than self."),
        ("Sadness", "The grief was total. It left no room for anything else.",
         "I tried to make space for other things.\nHappiness. Purpose. Small pleasures.\n\n"
         "The grief filled every corner before I could unpack them."),
        ("Sadness", "I lived inside my sadness for years.",
         "Not beside it. Inside it.\nIt was the walls and the ceiling and the floor.\n\n"
         "Everything I saw, I saw through it."),
        ("Sadness", "There was a weight I could never fully put down.",
         "I tried.\nI rested it on tables and beds and other people's shoulders.\n\n"
         "But it always found its way back.\nAlways settled back into my arms\nlike something that had chosen me."),
        ("Sadness", "The loss was immeasurable. I never recovered.",
         "I do not say that with bitterness.\nOnly with honesty.\n\n"
         "Some things cannot be recovered from.\nThey can only be survived.\nI survived. Barely."),
        ("Sadness", "Sorrow was the language I became fluent in.",
         "I learned to speak it without thinking.\nTo move through the world in it.\n\n"
         "I did not mean to.\nBut loss teaches what it will."),
        ("Sadness", "I missed people so much it felt like a physical place.",
         "A country I had been exiled from.\nA room I could no longer enter.\n\n"
         "I stood at the threshold for years,\nmy hand on a door that no longer existed."),
        ("Sadness", "The sadness was not occasional. It was constant.",
         "Not always loud.\nSometimes just a hum. But always there.\n\n"
         "Underneath the conversations.\nUnderneath the meals.\nUnderneath the ordinary days\nthat looked fine from the outside."),
        ("Sadness", "I built my entire life around the shape of my grief.",
         "Everything I chose, I chose to accommodate it.\n\n"
         "It was an extraordinary amount of power\nto give to sorrow."),
        ("Sadness", "By the end, the sadness was all I had left that was mine.",
         "Everything else had been taken,\nor given away, or simply worn away by time.\n\n"
         "But the sadness remained.\nIt was faithful, in its way.\nI will give it that."),
    ],

    ('anger', 5): [
        ("Anger", "A small irritation. Nothing I couldn't manage.",
         "Like a stone in your shoe\nyou never quite stop to remove.\n"
         "It pricked at me now and then.\n\nI waved it off. Mostly."),
        ("Anger", "Some things annoyed me. I let them.",
         "Briefly. Quietly.\nThe way you let a cloud cross the sun before moving on.\n\n"
         "I did not dwell. Dwelling seemed like a waste."),
        ("Anger", "A flicker of frustration, now and then.",
         "Nothing that lasted.\nJust a small flame\nthat came and went without leaving a mark.\n\n"
         "I was, mostly, fine."),
        ("Anger", "Irritation was a minor key in the symphony of my days.",
         "Present. Audible, if you listened closely.\nBut not the melody.\n\n"
         "Just background."),
        ("Anger", "I got annoyed. Then I got over it.",
         "That was my pattern.\nA brief flare. A breath. And then: over it.\n\n"
         "I was good at that.\nI was proud of being good at that."),
        ("Anger", "Minor grievances, quickly released.",
         "I did not collect them.\nI let them go, one by one,\nbefore they could accumulate."),
        ("Anger", "Mild frustration was as far as it usually went.",
         "A raised eyebrow. A sigh.\nThe internal monologue that says: really?\n\n"
         "And then: fine. Let it go."),
        ("Anger", "I noticed the unfairness. I did not dwell on it.",
         "It was there. Obviously.\nBut I chose, mostly,\nnot to give it more attention than it deserved."),
        ("Anger", "Something bristled in me, occasionally.",
         "A small defensive response.\nA reflex, more than a feeling.\n\n"
         "I noticed it.\nThen I put it back where it came from."),
        ("Anger", "Friction, now and then. Nothing more.",
         "Life has rough patches.\nI encountered mine.\nRan my hand across them, felt the texture, moved on.\n\n"
         "They were real. They were also small."),
    ],

    ('anger', 10): [
        ("Anger", "I had my frustrations. Who doesn't?",
         "I kept my temper — most of the time.\nBut it simmered beneath the surface,\n"
         "quiet and patient,\n\nwaiting for something to stir it."),
        ("Anger", "There were things I found genuinely unfair.",
         "I was right about most of them.\n\n"
         "But being right and being heard are different things.\nI learned that slowly, and not gracefully."),
        ("Anger", "My patience had a limit. I found it occasionally.",
         "I tried not to.\nBut sometimes the limit found me first.\n\n"
         "I was not proud of those moments.\nBut I was not entirely ashamed, either."),
        ("Anger", "I bit my tongue. Regularly. It left marks.",
         "The things I did not say\naccumulated somewhere behind my teeth.\n\n"
         "I imagine they are still there,\nwaiting to be said to no one in particular."),
        ("Anger", "I was frustrated by the gap between what was and what should be.",
         "That gap was always there.\nAlways visible.\nI pointed at it sometimes.\n\n"
         "No one seemed to see what I saw."),
        ("Anger", "The anger was manageable. Mostly contained.",
         "I had techniques.\nBreathing. Walking. The pause before the response.\n\n"
         "They worked. Usually.\nNot always. But usually."),
        ("Anger", "I felt injustice keenly. I responded proportionately.",
         "Most of the time.\n\n"
         "There were exceptions.\nI am aware of them.\nI am also aware that I was often right to be angry."),
        ("Anger", "Resentment visited but did not move in.",
         "I showed it the door. Repeatedly.\n\n"
         "It kept knocking.\nBut I kept answering,\nand eventually it stopped coming."),
        ("Anger", "I had opinions about the way things were handled.",
         "Strong ones.\nI shared some of them.\n\n"
         "The rest I carried, which was heavy in its own way.\nBut quieter."),
        ("Anger", "Some situations made me clench my jaw.",
         "I noticed. I breathed. I unclenched.\n\n"
         "Repeat as necessary.\nAnd it was necessary, regularly.\nMore than I would have liked."),
    ],

    ('anger', 20): [
        ("Anger", "I was furious at the unfairness of it all.",
         "I bit my tongue until it bled.\nThe injustice sat in my chest like a stone,\n"
         "heavy and hot and impossible to swallow.\n\nI never said half of what I meant to."),
        ("Anger", "The anger was a fire that did not need much to ignite.",
         "A look. A word. A pattern repeated one too many times.\n\n"
         "I burned often.\nI burned clearly.\nI was not always wrong."),
        ("Anger", "I fought things that deserved to be fought.",
         "I was not always graceful. I was not always kind.\n\n"
         "But I was right more often\nthan people were willing to admit,\nand that kept me going."),
        ("Anger", "My anger was righteous and exhausting in equal measure.",
         "I stood for things.\nLoud things. Clear things.\n\n"
         "It cost me relationships.\nIt cost me sleep.\nI would do most of it again."),
        ("Anger", "I was angry at what people got away with.",
         "At the comfortable silence of those who could have spoken.\nAt the shrug that passes for acceptance.\n\n"
         "I could not shrug. I tried. I failed."),
        ("Anger", "The injustice was real and so was my response to it.",
         "I want that noted.\nI was not overreacting.\n\n"
         "The audience disagreed.\nThe audience was wrong."),
        ("Anger", "I spent years arguing with people who refused to see.",
         "I was tired by the end.\nBut I do not regret the arguments.\n\n"
         "Someone has to make the noise.\nI was willing to be that person."),
        ("Anger", "My anger shaped everything I built and everything I broke.",
         "I built things with it — momentum, change, boundaries.\n\n"
         "I also broke things with it.\nRelationships. Opportunities.\nA few doors I wish I had not slammed."),
        ("Anger", "I raged at the things I could not change.",
         "That was the worst of it.\nAll that heat, and nowhere for it to go.\n\n"
         "I learned, eventually, to direct it.\nBut it took longer than it should have."),
        ("Anger", "I was furious. I had good reason to be.",
         "I will not pretend otherwise.\nThe anger was earned.\nEvery degree of it.\n\n"
         "What I did with it — that is the question\nI am still trying to answer."),
    ],

    ('anger', 30): [
        ("Anger", "The rage consumed me. I could not let it go.",
         "It burned and burned and never went out.\nI tried to put it down.\n"
         "It always found its way back into my hands.\n\nIn the end, it was all I had left."),
        ("Anger", "I was made of fury by the end.",
         "It had replaced things — patience, softness, hope.\nOne by one, unnoticed,\n"
         "until all that remained was the burning.\n\nI do not know who I was before it."),
        ("Anger", "The anger was total. It left no room for doubt.",
         "I was certain.\nAbsolutely, completely certain.\n\n"
         "About the wrong. About the blame.\nThat certainty was both my armour and my prison."),
        ("Anger", "I was at war with the world for most of my life.",
         "Not always loudly. But always.\n\n"
         "A permanent readiness.\nA constant bracing.\nAs if the next blow was always already incoming."),
        ("Anger", "The rage was inherited and then refined.",
         "It came from somewhere — a wound, a history.\nI did not choose it.\n\n"
         "But I fed it.\nCarefully. Thoroughly. For decades."),
        ("Anger", "I burned relationships down with my anger.",
         "Not carelessly. Deliberately.\nWith full knowledge of what I was doing.\n\n"
         "And still I could not stop.\nThe fire wanted what it wanted."),
        ("Anger", "My fury was the most alive I ever felt.",
         "I am ashamed to say it.\nBut I am trying to be honest.\n\n"
         "When I was angry, I was real.\nPowerful. Present.\nAt least I was something."),
        ("Anger", "Nothing ever cooled it. Nothing ever lasted.",
         "Resolution. Forgiveness. Distance.\nI tried all of them.\n\n"
         "The anger waited.\nPatient as stone.\nI always returned."),
        ("Anger", "I gave my best years to a fury I could not name.",
         "I only knew it was there.\nThat it was mine.\nThat I could not put it down\nwithout losing myself entirely.\n\n"
         "Or so I believed."),
        ("Anger", "The rage outlasted everything else.",
         "Love. Hope. The capacity for rest.\nThey went, one by one.\n\n"
         "The rage remained.\nFaithful, in its terrible way.\nThe last thing standing."),
    ],

    ('fear', 5): [
        ("Fear", "A shiver now and then. Nothing serious.",
         "The kind of worry you wave away before sleep.\nA shadow at the edge of the room\n"
         "that disappears when you look directly at it.\n\nI told myself it was nothing."),
        ("Fear", "Mild anxiety. Nothing I could not outrun.",
         "It visited mostly at night.\nA gentle unease.\nThe sense that I had forgotten something important.\n\n"
         "I never remembered what it was."),
        ("Fear", "A small wariness. Practical, even.",
         "I double-checked things.\nLooked both ways twice.\nRead the fine print.\n\n"
         "I called it caution.\nMaybe it was. Maybe it was something slightly more."),
        ("Fear", "The occasional worry that passed quickly.",
         "A flutter before a decision.\nA hesitation before a risk.\n\n"
         "Normal, I think.\nHuman, certainly.\nNothing to write home about."),
        ("Fear", "Something occasionally made me hesitate.",
         "A pause before certain doors.\nA brief calculation: is this safe?\n\n"
         "Usually it was.\nI entered anyway.\nI was usually glad I did."),
        ("Fear", "A light caution that kept me sensible.",
         "I was not reckless.\nI thought before I leaped.\n\n"
         "Whether that was wisdom or timidity,\nI am not entirely sure.\nBoth, probably."),
        ("Fear", "Minor dread. The kind that dissolves by morning.",
         "It gathered in the evenings.\nSomething undefined. Unnamed.\n\n"
         "By the time the light came back, it had already gone."),
        ("Fear", "I was alert, perhaps. Cautious, certainly.",
         "There is nothing wrong with alertness.\nI told myself that often.\n\n"
         "It was true.\nBut it was also, sometimes, exhausting."),
        ("Fear", "The worry was small and I managed it well.",
         "I had strategies.\nThoughts that helped.\nRituals that settled things.\n\n"
         "I was competent at managing my small fear.\nI think that counts for something."),
        ("Fear", "A distant alarm. Faint. Easily ignored.",
         "I ignored it.\nMostly successfully.\n\n"
         "It was not always wrong to sound.\nBut it was often louder than necessary."),
    ],

    ('fear', 10): [
        ("Fear", "Something always made me uneasy.",
         "I checked the locks twice.\nLooked over my shoulder in empty hallways.\n"
         "I couldn't explain it to anyone.\n\nThey wouldn't have understood."),
        ("Fear", "There was a background hum of anxiety I never fully silenced.",
         "I learned to function around it.\nTo carry it like a bag\nyou stop noticing the weight of.\n\n"
         "It was always there."),
        ("Fear", "Uncertainty was a particular torment.",
         "I did not handle not-knowing well.\nThe gap between what was\nand what might happen felt wider than it was.\n\n"
         "I fell into it regularly."),
        ("Fear", "I worried about things before they happened.",
         "Extensively. Elaborately. With great attention to detail.\n\n"
         "I was often wrong about what would go badly.\nBut I was always thorough."),
        ("Fear", "Dread arrived before reason could intervene.",
         "A quick student.\nPresent before I had finished forming the thought.\n\n"
         "I spent a great deal of energy\ntrying to catch up to my own fear."),
        ("Fear", "I was braced, always, for something to go wrong.",
         "It made me good in a crisis.\nI was already ready.\n\n"
         "It made everyday life harder.\nBeing always ready is exhausting\nwhen nothing is happening."),
        ("Fear", "Certain situations filled me with a dread I could not justify.",
         "I tried to explain it.\nThe explanations were never quite right.\n\n"
         "The dread, however, was extremely accurate."),
        ("Fear", "I imagined the worst regularly and in detail.",
         "I told myself it was preparation.\nSometimes it was.\n\n"
         "Often it was just suffering in advance\nfor things that never arrived."),
        ("Fear", "Trust did not come easily to me.",
         "I wanted to give it.\nI tried, sometimes, to give it.\n\n"
         "But there was always a part of me\nwaiting to be proven right to have withheld it."),
        ("Fear", "Anxiety was the tax I paid on caring about things.",
         "Everything I loved, I feared losing.\nEvery good thing felt provisional.\n\n"
         "I was not wrong, exactly.\nBut I was not at peace, either."),
    ],

    ('fear', 20): [
        ("Fear", "The dread was constant. Always braced for impact.",
         "I lived on the edge of something I couldn't name.\nEvery phone call felt like bad news arriving.\n"
         "Every silence felt like it was about to break.\n\nI was tired of being afraid."),
        ("Fear", "Fear organised my life without my permission.",
         "It decided where I went.\nWhat I tried.\nWho I let in.\n\n"
         "I thought I was making choices.\nI was mostly making accommodations."),
        ("Fear", "I was afraid of so many things.",
         "Losing people. Making mistakes.\nBeing seen clearly and found wanting.\n\n"
         "The list was long.\nI had it memorised.\nI wish I had burned it."),
        ("Fear", "The anxiety was significant enough to be a presence.",
         "A third person in every room.\nIn every decision.\nIn every conversation that mattered.\n\n"
         "I had to talk around it constantly."),
        ("Fear", "I spent years flinching at things that had not happened.",
         "The fear was of the future.\nA specific, terrible, detailed future\nthat my mind had constructed with great care.\n\n"
         "It never arrived.\nBut it cost me years."),
        ("Fear", "Safety was something I searched for constantly and rarely found.",
         "Not physical safety.\nThe other kind.\nThe kind that comes from inside.\n\n"
         "I did not have that.\nI looked for it in other people.\nThey could not give it."),
        ("Fear", "I was hypervigilant. It wore me out.",
         "Watching everything.\nTracking every shift in the room.\nReading every face.\n\n"
         "I was very good at detecting danger.\nI was very bad at rest."),
        ("Fear", "The fear narrowed my world considerably.",
         "Places I would not go.\nThings I would not try.\nPeople I would not meet.\n\n"
         "The list of the unlived grew slowly,\npatiently, over years."),
        ("Fear", "I waited for the other shoe to drop for most of my life.",
         "Even when things were good.\nEspecially when things were good.\n\n"
         "I could not enjoy it.\nI was too busy listening for the fall."),
        ("Fear", "Every good thing came wrapped in its potential loss.",
         "I could not receive anything freely.\nGifts arrived with their future absence.\n\n"
         "I loved people and simultaneously grieved them.\nIt was an inefficient way to live."),
    ],

    ('fear', 30): [
        ("Fear", "I was terrified. Every shadow. Every sound.",
         "Fear was my oldest companion,\nand the cruelest.\n"
         "It never left me alone — not even at the end.\n\nEspecially not at the end."),
        ("Fear", "Terror was the water I swam in.",
         "I did not know, for a long time,\nthat other people were not swimming.\n\n"
         "I thought the water was normal.\nI thought everyone was this afraid."),
        ("Fear", "Fear was not a visitor. It was a resident.",
         "It had moved in early.\nIt had opinions about the furniture.\n\n"
         "By the time I realised what it was,\nit had been there so long\nI had forgotten what the space looked like without it."),
        ("Fear", "I was afraid of being afraid.",
         "A loop with no exit.\n\n"
         "The fear of the fear made everything worse.\nMade every small anxiety\ninto evidence of something catastrophic.\nI could not find the door."),
        ("Fear", "The world felt dangerous in every direction.",
         "Not occasionally. Not when the evidence supported it.\nConstantly. Fundamentally.\n\n"
         "As if danger were the default state\nand safety were the aberration."),
        ("Fear", "I constructed my life around what I was afraid of.",
         "Every choice was a negotiation with the fear.\n\n"
         "Where to live so I would feel safe.\nWhat work to do so I would not be exposed.\n\n"
         "It took everything."),
        ("Fear", "I could not be calm. I had forgotten how.",
         "Rest felt dangerous.\nRelaxing felt like lowering my guard.\n\n"
         "I stayed tense for so long\nthat tension became my resting state."),
        ("Fear", "Everything I loved, I feared losing with a ferocity that exhausted me.",
         "Not reasonable caution.\nSomething wilder than that.\n\n"
         "A certainty that the good things\nwere always already leaving.\nAlready almost gone."),
        ("Fear", "The fear spoke louder than anything else.",
         "Louder than reason.\nLouder than love.\nLouder than the evidence\nthat I had survived every previous thing.\n\n"
         "It was the loudest voice in the room.\nAlways."),
        ("Fear", "I was not brave. I want to be honest about that.",
         "I was not the person who walked toward the difficult thing.\nI was the person\nwho learned, slowly and painfully,\nhow to walk toward it anyway.\n\n"
         "That is not the same as bravery.\nBut it is something."),
    ],
}

class Ghost:

    EMOTIONS = ('happiness', 'sadness', 'fear', 'anger')

    _LINKED_PAIRS = [
        ('happiness', 'fear'),
        ('sadness', 'happiness'),
        ('anger', 'sadness'),
        ('fear', 'anger'),
    ]

    def __init__(self):
        self.happiness = 0
        self.sadness = 0
        self.fear = 0
        self.anger = 0
        self._assign_emotions()

    def _assign_emotions(self):
        low_primary, low_secondary = random.choice(self._LINKED_PAIRS)

        remaining = [e for e in self.EMOTIONS if e not in (low_primary, low_secondary)]
        random.shuffle(remaining)
        high_primary, high_secondary = remaining

        setattr(self, low_primary,   10)
        setattr(self, low_secondary,  5)
        setattr(self, high_primary,  30)
        setattr(self, high_secondary, 20)

    @property
    def stats(self) -> dict:
        return {e: getattr(self, e) for e in self.EMOTIONS}

    def get_hint_clue(self, emotion: str) -> tuple:
        if emotion not in self.EMOTIONS:
            raise ValueError(f"Unknown emotion: {emotion!r}")
        value   = getattr(self, emotion)
        options = GHOST_CLUES.get((emotion, value))
        if not options:
            return (emotion.capitalize(), "...", "No message found.")
        return random.choice(options)

    def get_hint_card_path(self, emotion: str) -> str:
        if emotion not in self.EMOTIONS:
            raise ValueError(f"Unknown emotion: {emotion!r}")
        value = getattr(self, emotion)
        return f"Game_png/Card_Ghost/{emotion}_{value}.jpg"

    def __repr__(self):
        stats = ", ".join(f"{e}={getattr(self, e)}" for e in self.EMOTIONS)
        return f"Ghost({stats})"