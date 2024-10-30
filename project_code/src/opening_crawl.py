import time

def display_opening_crawl():
    crawl_text = """
================================================================================
                                A LONG TIME AGO,
                               IN A GALAXY FAR,
                                  FAR AWAY...

================================================================================

                               *** STAR WARS RPG ***
================================================================================
                                     EPISODE I

                             THE FORCE RISES AGAIN...

================================================================================

A galaxy in turmoil, ruled by the shadow of the Empire. With rebel whispers 
and calls for freedom growing, a few brave heroes are called upon to restore 
hope and unveil secrets long buried. Their journey begins on the mystical 
planet of JEDHA, a place of ancient relics and dangerous forces...

================================================================================

                               *** YOUR MISSION ***
================================================================================

Assemble a team of courageous allies, each with their own past, talents, and 
desires. Navigate their fates through trials that only the strongest, 
wisest, and most cunning can overcome. From the eerie depths of JEDHA to 
the metallic corridors of the IMPERIAL STAR DESTROYER, you will face decisions 
that test not only skill but also loyalty and resolve.

================================================================================

                               *** CHOOSE YOUR HEROES ***
================================================================================

In this adventure, every character has a story, a purpose, and a power to wield. 
Choose wisely; their strengths—and weaknesses—will shape the path ahead.

1. **JEDI** - Guardians of the Force, wielders of ancient powers. With their 
   Lightsabers and profound Mind Tricks, they stand as symbols of hope.
   - Skills: Force Sensitivity, Mind Tricks, Lightsaber Proficiency
   - Strengths: Deep connection with the Force, high combat ability

2. **BOUNTY HUNTER** - Mercenaries with razor-sharp reflexes and a thirst for 
   adventure. Hardened by survival, they’ll fight any foe for the right price.
   - Skills: Dexterity, Blaster Proficiency, Piloting
   - Strengths: Agile, adaptable, skilled in ranged and close combat

3. **DROID** - Metallic, resilient, and always logical. Droids think with circuits 
   and act with precision, often hacking their way to victory.
   - Skills: Processing, Hacking, Technical Support
   - Strengths: High intelligence, unmatched in technology and data handling

4. **REBELS & ROYALTY** - Fighters, leaders, and dreamers. Driven by a desire to 
   restore peace, they are bold in both intellect and action.
   - Skills: Leadership, Strategy, Diplomatic Persuasion
   - Strengths: Versatile, strategic, capable of uniting and inspiring allies

================================================================================

                              *** THE WORLD OF JEDHA ***
================================================================================

JEDHA, an arid and desolate planet, was once a sacred home to ancient Force-users. 
Scattered ruins and Imperial patrols make it a dangerous place for rebels. 
Through the twisted paths and crumbling temples, your heroes will uncover relics, 
face Imperial soldiers, and learn of a hidden power that could change the galaxy.

As you progress, beware of:
- **Imperial Scouts** – They search for anyone suspicious. Stealth and quick 
  thinking are essential here.
- **Ancient Guardians** – Relics come with their own protectors. Test your 
  resolve to avoid their wrath.
- **Force-sensitive Trials** – Only those with knowledge of the Force will 
  understand these mysterious rites.

The path will lead you closer to the ultimate mission but also to the final 
event on JEDHA, **DOCKED_INSIDE**: an intense battle to secure a stolen shuttle 
and escape to the dreaded STAR DESTROYER.

================================================================================

                        *** AWAITING ON THE STAR DESTROYER ***
================================================================================

Hidden deep in Imperial space, a STAR DESTROYER harbors secrets too dark 
and powerful to ignore. Only the most skilled can infiltrate it and retrieve 
the information necessary to strike a blow to the Empire.

Expect:
- **Elite Imperial Guards** – Stronger and faster than any foe on JEDHA.
- **Dark Secrets** – Forbidden knowledge and forbidden power.
- **Critical Choices** – Decisions here will not just affect your heroes but 
  the entire rebellion’s future.

================================================================================

                                *** GAMEPLAY & EVENTS ***
================================================================================

As you journey, each event will offer choices:
1. **CHOOSE YOUR PARTY** - Select your heroes carefully to face each challenge.
   Balance their unique skills to overcome varied trials and maximize success.

2. **NAVIGATE EVENTS** - Each test of skill demands the best of your team. Use 
   their attributes wisely to pass, partially succeed, or fail.

3. **OUTCOME AND CONSEQUENCE** - Every event has repercussions:
   - Pass - Advance confidently and gain trust and respect.
   - Partial Pass - Move forward but with lingering challenges or risks.
   - Fail - Too many failures will lead to dire consequences. Success is not 
     guaranteed, and too many mistakes may result in game over.

================================================================================

                           THE FATE OF THE GALAXY AWAITS...
================================================================================

Will you and your team rise to the challenge? Will you uncover the hidden powers 
on JEDHA and unlock the mysteries on the STAR DESTROYER? The Dark Side is powerful, 
and only the bravest and most loyal can resist its influence.

================================================================================
                                   MAY THE FORCE 
                                     BE WITH YOU

================================================================================
"""
    for line in crawl_text.splitlines():
        print(line)
        time.sleep(0.1)  # Adjust this value for slower/faster effect

    input("\nPress Enter to begin your adventure...")  # Prompt to start the game
