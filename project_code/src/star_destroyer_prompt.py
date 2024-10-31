import time
import os

def display_star_destroyer_prompt():
    star_destroyer_ascii = r"""
        .            .                     .
                        _        .                          .            (
                        (_)        .       .                                     .
        .        ____.--^.
        .      /:  /    |                               +           .         .
                /:  `--=--'   .                                                .
        LS    /: __[\==`-.___          *           .
            /__|\ _~~~~~~   ~~--..__            .             .
            \   \|::::|-----.....___|~--.                                 .
            \ _\_~~~~~-----:|:::______//---...___
        .   [\  \  __  --     \       ~  \_      ~~~===------==-...____
            [============================================================-
            /         __/__   --  /__    --       /____....----''''~~~~      .
        *    /  /   ==           ____....=---='''~~~~ .
            /____....--=-''':~~~~                      .                .
            .       ~--~           .           .        *            .
                            .                                   .           .
                                .                      .             +
            .     +              .                                       <=>
                                                    .                .      .
        .                 *                 .                *                ` -
        """
    description = (
        "As you stand victorious on the desolate surface of Jedha, the ground trembles\n"
        "beneath your feet. In the distance, a colossal shadow emerges from the horizon—\n"
        "the Imperial Star Destroyer, a symbol of the Empire's might and relentless pursuit\n"
        "of power. Its angular silhouette looms menacingly, dwarfing the landscape as it\n"
        "approaches with purpose.\n\n"
        "Inside its dark corridors, the Emperor's most sinister plans unfold. The Empire seeks\n"
        "to harness the ancient power of the Kyber Crystals found on Jedha, using their energy\n"
        "to fuel a new generation of superweapons that could obliterate entire worlds. This\n"
        "Star Destroyer, with its fleet of TIE Fighters and battalions of stormtroopers,\n"
        "is poised to exert control over the galaxy, striking fear into the hearts of the\n"
        "Rebellion.\n\n"
        "Your next challenge lies within the steel walls of this imperial fortress. Will you\n"
        "be able to thwart their plans and save the galaxy from tyranny?\n"
    )

    # Clear the terminal for a better effect
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Scroll the ASCII art first
    for line in star_destroyer_ascii.splitlines():
        print(line)
        time.sleep(0.05)  # Adjust this value for slower/faster effect

    # Add space between ASCII art and description
    print("\n" + "=" * 70 + "\n")  

    # Scroll the description line by line
    for line in description.splitlines():
        print(line)
        time.sleep(0.05)  # Adjust this value for slower/faster effect

    input("\nPress Enter to begin your mission on the IMPERIAL STAR DESTROYER...")  # Prompt to start the game
