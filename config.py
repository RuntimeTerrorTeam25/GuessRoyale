# config.py

MAX_LIVES = 3

# Difficulty settings for both modes
# For number mode: use min, max, max_attempts
# For word mode: use max_attempts only
DIFFICULTY_LEVELS = {
    "1": {"key": "1", "name": "Easy",   "min": 1,  "max": 20,  "max_attempts": 7},
    "2": {"key": "2", "name": "Medium", "min": 1,  "max": 50,  "max_attempts": 6},
    "3": {"key": "3", "name": "Hard",   "min": 1,  "max": 100, "max_attempts": 5},
}

# Simple built-in word lists per difficulty
WORD_LISTS = {
    "1": [
        "cat","sun","pen","ball","tree","fish","frog","book","lamp","star",
        "ship","rain","milk","door","bird","wind","seed","moon","rock",
        "note","ring","coat","snow","cake","pear","corn","wolf","duck",
        "leaf","shoe","bell","soap","glue","road","hill","fork","coin",
        "bell","nest","shoe","rope","frog","vine","seed","cake","flag",
        "wall","tent","bowl","spoon","plate","chair","bread","grass",
        "horse","goat","fire","desk","palm","kite","boat","lego",
        "sand","wave","clay","moss","gate","twig","ruby","opal","spin",
        "snap","drop","step","jump","bark","meow","buzz","clap","sing",
        "draw","fold","pour","mix","cook","bake","wipe","peel","roll",
        "push","pull","ring","yarn","sock","honey"
    ],

    "2": [
        "apple","train","cloud","river","planet","forest","castle","bottle","bridge","silver",
        "garden","flower","jungle","island","ocean","market","museum","dancer","artist","yellow",
        "throat","middle","circle","pocket","window","camera","travel","moment","friend","family",
        "singer","writer","danger","vision","motion","handle","branch","animal","fabric","pepper",
        "sudden","header","thirst","marble","future","rocket","planet","glider","switch","charge",
        "hunter","farmer","saddle","doctor","school","pillow","winter","summer","autumn","spring",
        "branch","thread","remote","button","engine","shield","smooth","spirit","energy","mirror",
        "butter","cheese","noodle","cookie","fruits","basket","socket","candle","planet","stream",
        "custom","strand","copper","timber","powder","margin","signal","random","forest","folder"
    ],

    "3": [
        "python","galaxy","neuron","quantum","royale","gravity","horizon","mystery","crystal","biology",
        "stellar","orbiting","magnetic","voltage","quantum","parallel","infinite","spectrum","polygon","organic",
        "electro","protein","network","virtual","cluster","integer","decimal","calcium","silicon","element",
        "resolve","fracture","circuit","pattern","dynamic","compute","formula","theorem","diamond","emerald",
        "nebulae","asteroid","synapse","quantum","particle","density","entropy","fractal","tension","momentum",
        "kinetic","version","upgrade","machine","storage","process","compiler","algorithm","variable","function",
        "terminal","photon","glucose","plasma","volcano","turbine","capsule","reality","fiction","digital",
        "quantize","simulate","generate","optical","harmonic","acoustic","synergy","spectra","magenta","vortex",
        "galactic","magmatic","ceramic","complex","oxidize","hydrate","thermal","neutral","volumic","cascading"
    ]
}

LEADERBOARD_FILE = "leaderboard.json"
