from pathlib import Path
from typing import List, Set, TypedDict, Optional

import networkx as nx

from community_conflict import Node
from community_conflict.cache import read_or_parse_file
from community_conflict.collapse import collapse, contraction_weighted_on_keyword_similarity


class CommunityDefinition(TypedDict):
    name: str
    common_nodes: Set[str]


COMMUNITIES: List[CommunityDefinition] = [
    {
        "name": "Arts",
        "common_nodes": {"music", "books", "movies", "fantasy", "writing", "guitar"}
    },
    {
        "name": "Pop Culture",
        "common_nodes": {"starwars", "marvel", "harrypotter", "thelastairbender", "gameofthrones"}
    },
    {
        "name": "Technology",
        "common_nodes": {"pcmasterrace", "android", "diy", "programming", "linux", "learnprogramming", "apple", "programminghumor", 'python', 'web_design', 'machinelearning', "java", "cpp"}
    },
    {
        "name": "Generic Reddit",
        "common_nodes": {"askreddit", "pics", "bestof", "funny", "todayilearned", "videos", "gifs", "wtf"}
    },
    {
        "name": "Science and Space",
        "common_nodes": {"kerbalspaceprogram", "spacex", "microbiology", "mars"}
    },
    {
        "name": "Sports",
        "common_nodes": {"nfl", "nba", "cfb", "hockey", "sports", "baseball", "collegebasketball", "patriots"}
    },
    {
        "name": "Fitness",
        "common_nodes": {'fitnesscirclejerk', 'fitness', 'bicycling', 'mma', 'loseit', 'running', 'bodybuilding', 'climbing', 'bodyweightfitness', 'martialarts'}
    },
    {
        "name": "Money",
        "common_nodes": {'bitcoin', 'dogecoin', 'buttcoin', 'cryptocurrency', 'btc', 'ethereum', 'wallstreetbets', 'investing', 'business', 'dogemarket', 'beermoney', 'reddoge'}
    },
    {
        "name": "Relationships",
        "common_nodes": {'relationships', 'personalfinance', 'offmychest', 'sex', 'ama', 'getmotivated', 'theredpill', 'thebluepill', 'nofap', 'depression', "lgbt", "suicidewatch", "asktransgender"}
    },
    {
        "name": "Fashion",
        "common_nodes": {'malefashionadvice', 'makeupaddiction', 'streetwear', 'skincareaddiction', 'watches', 'edc', 'fountainpens', 'buyitforlife', 'sneakers', 'frugalmalefashion', 'femalefashionadvice', 'asianbeauty', 'wicked_edge', 'notebooks', 'fashionreps'}
    },
    {
        "name": "Gaming",
        "common_nodes": {'gaming', 'leagueoflegends', 'games', 'dota2', 'globaloffensive', 'overwatch', 'peoplewhosayheck', 'smashbros', 'hearthstone', 'excgarated', 'oculus', 'destinythegame', 'ps4', 'wow', 'pcgaming', 'xboxone', 'tf2', 'gamedev', 'steam', 'gamingcirclejerk'}
    },
    {
        "name": "Countries",
        "common_nodes": {'newsokur', 'japancirclejerk', 'china', 'newsokunomoral', 'japan', 'translator', 'asianamerican', 'ccj2', 'korea', 'languagelearning', 'kpop', 'aznidentity', 'asianmasculinity', 'bakanewsjp', '5555555', 'yellowperil', 'sino', 'hongkong', 'botrights', 'learnjapanese'}
    },
    {
        "name": "Minecraft",
        "common_nodes": {'minecraft', 'civcraft', 'mcservers', 'feedthebeast', 'ultrahardcore', 'mindcrack', 'civilizatonexperiment', 'devoted', 'hcfactions', 'minecraftsuggestions', 'lordsofminecraft', 'mindcrackcirclejerk', 'admincraft', 'mtaugusta', 'hcteams', 'danzilona', 'feedthebeastservers'}
    },
    {
        "name": "Liquor",
        "common_nodes": {'cigars', 'wine', 'bourbon', 'pipetobacco', 'cocktails', 'bartenders', 'scotch', 'alcohol', 'whiskey', 'whiskyinventory', 'whiskyporn'}
    },
    {
        "name": "'Merica",
        "common_nodes": {'cars', 'motorcycles', 'guns', 'subreddit_stats', 'travel', 'assistance', 'seattle', 'losangeles', 'portland', 'atlanta', 'unresolvedmysteries', 'boston', 'austin', 'philippines', 'denver', 'teslamotors', 'justrolledintotheshop', 'freebies', 'washingtondc', 'beer', 'dallas', 'firearms', 'rbi', 'sandiego', 'newjersey', 'homebrewing', 'campingandhiking', 'multicopter'}
    },
    {
        "name": "Something 1",
        "common_nodes": {'playark', 'playarkservers', 'ark', 'projectmilsim', 'survivetogether', 'arkone', 'findaunit', 'ark_pc', 'arkfactions', 'playarklfg', 'funkark', 'zodiacfalls', 'jurassickingdoms', 'battleroyalegames', 'badneighbor'}
    },
    {
        "name": "DnD and Board Games",
        "common_nodes": {'dnd', 'magictcg', 'worldbuilding', 'boardgames', 'rpg', 'lfg', 'itsadndmonsternow', 'dndnext', 'pathfinder_rpg', 'dndbehindthescreen', 'warhammer40k', 'gametales', 'shadowrun', 'warhammer', 'spikes', 'magicthecirclejerking', 'lovecraft', 'tabletopgamedesign', 'modernmagic', 'roleplay'}
    },
    {
        "name": "Religion",
        "common_nodes": {'exmormon', 'exjw', 'mormon', 'saltlakecity', 'latterdaysaints', 'exchristian', 'scientology', 'utah', 'exittors', 'atheistvids', 'cults', 'excatholic', 'exjew', 'lds'}
    },
    {
        "name": "Porn",
        "common_nodes": {'tipofmypenis', 'gonewild', 'gonewildaudio', 'r4r', 'dirtypenpals', 'nsfw_gif', 'nsfw', 'bdsmcommunity', 'gonewildstories', 'realgirls', 'incest'}
    },
    {
        "name": "Clash of Clans",
        "common_nodes": {'clashofclans', 'clashroyale', 'clashofclansrecruit', 'redditomicron', 'yesno', 'clashofclansmu', 'redditclansystem', 'redditbandits', 'redditraiderscoc', 'redditstrike', 'redditallianceclans', 'rwcs', 'redditiota', 'clanxenon', 'clanredditomega'}
    },
    {
        "name": "Writing and Arts",
        "common_nodes": {'writingprompts', 'nosleep', 'hfy', 'paranormal', 'codes', 'scp', 'arg', 'shortscarystories', 'ufos', 'letsnotmeet', 'rational', 'ocpoetry', 'picturegame', 'parahumans', 'poetry'}
    },
    {
        "name": "Political",
        "common_nodes": {'subredditdrama', 'worldnews', 'news', 'drama', 'the_donald', 'conspiracy', 'science', 'politics', 'technology', 'dataisbeautiful', 'shitamericanssay', 'askhistorians', 'circlebroke2', 'sandersforpresident', 'atheism', 'india', 'changemyview', 'europe', 'futurology', 'nottheonion'}
    },
    {
        "name": "Something 3",
        "common_nodes": {'thebutton', 'joinrobin', 'periwinkle', 'robintracking', 'orangered', 'agario', 'knightsofthebutton', 'diepio', 'team60s', 'buttonaftermath', 'worldproblems', 'buttonnews', 'emerald_council', 'thedarkmountain', 'unitedcolors'}
    },
    {
        "name": "Vaping",
        "common_nodes": {'electronic_cigarette', 'ecigclassifieds', 'vaping', 'diy_ejuice', 'flashlight', 'ecr_eu', 'ecig_vendors', 'canadian_ecigarette', 'openpv', 'coilporn', 'vapeitforward'}
    },
    {
        "name": "Anime",
        "common_nodes": {'anime', 'whowouldwin', 'place', 'mlplounge', 'undertale', 'stevenuniverse', 'fivenightsatfreddys', 'jontron', 'mylittlepony', 'homestuck', 'respectthreads', 'mylittleandysonic1', 'manga', 'dbz', 'gravityfalls', 'naruto', 'rwby', 'onepiece', 'yugioh'}
    },
    {
        "name": "Pokemon",
        "common_nodes": {'pokemongo', 'pokemon', 'thesilphroad', 'twitchplayspokemon', 'pokemongodev', 'winnipeg', 'pokemongiveaway', 'tppkappa', 'ingress', 'pokemontrades', 'stunfisk', 'casualpokemontrades', 'pokemonplaza', 'shitgreeddisastersays', 'svexchange', 'poketradereferences', 'shinypokemon', 'pokemonexchangeref', 'pokemonromhacks', 'pokemongoyellow'}
    },
    {
        "name": "CIV",
        "common_nodes": {'civ', 'crusaderkings', 'paradoxplaza', 'civbattleroyale', 'eu4', 'stellaris', 'civhybridgames', 'hoi4', 'democraciv', 'cbrbattleroyale', 'cbrmodelworldcongress', 'civworldpowers', 'wastelandpowers', 'arumba07', 'civrapbattleroyale'}
    },
    {
        "name": "Reddit Meta",
        "common_nodes": {'help', 'trendingsubreddits', 'needamod', 'redditrequest', 'modhelp', 'automoderator', 'ideasfortheadmins', 'enhancement', 'botwatch', 'resissues', 'modsupport', 'changelog', 'redditdev', 'imaginarynetwork', 'tinysubredditoftheday', 'shadowban', 'shittheadminssay', 'blog', 'modclub', 'evex', 'requestabot', 'askmoderators'}
    },
    {
        "name": "Drugs",
        "common_nodes": {'trees', 'drugs', 'darknetmarkets', 'psychonaut', 'occult', 'buddhism', 'joerogan', 'gardening', 'meditation', 'nootropics', 'opiates', 'lsd', 'sorceryofthespectacle', 'badeasternphilosophy', 'vaporents', 'mandelaeffect', 'zen', 'drugscirclejerk'}
    },
    {
        "name": "Animal Crossing",
        "common_nodes": {'animalcrossing', 'ratemymayor', 'actrade', 'acbanhammer', 'camelhoarder101', 'adoptmyvillager', 'acqr', 'animalcrossingjerk', 'buddycrossing', 'acturnips', 'dreamcrossing', 'acduplication', 'achappyhome', 'katiecrossing', 'scjwithscotsman', 'achacks', 'acnlgroup'}
    },
    {
        "name": "Random 1",
        "common_nodes": {'shamisen', 'esotericos', 'uglytindergirls', 'overtalefangame', 'dogswithsunglasses', 'propagandamaps', 'carindi', 'adultdiapers', 'spiritwalkthegame', 'dmscape', 'winnipegsubreddits', 'shortskirt', 'tnsbigboybonanza', 'bitcoinlab', 'coxisms', 'sarahgadon', 'ymcmb', 'vegetableswitheyes', 'bottomofyoutube'}
    },
    {
        "name": "Guns",
        "common_nodes": {'guns', 'firearms', 'weekendgunnit', 'ccw', 'hunting', 'airsoft', 'ar15', 'gunsforsale', 'canadaguns', 'gundeals', 'a_irsoft'}
    },
    {
        "name": "Mobile Devices",
        "common_nodes": {'android', 'apple', 'jailbreak', 'gadgets', 'ipad', 'androidcirclejerk', 'iphone', 'androidapps', 'windowsphone', 'google', 'androidquestions', 'androidgaming', 'tmobile'}
    },
    {
        "name": "Multiplayer gaming",
        "common_nodes": {'leagueoflegends', 'dota2', 'globaloffensive', 'overwatch', 'hearthstone', 'wow', 'starcraft', 'runescape', 'twitch'}
    },
    {
        "name": "Audio and Music",
        "common_nodes": {'music', 'hiphopheads', 'tipofmytongue', 'kanye', 'listentothis', 'electronicmusic', 'wearethemusicmakers', 'hiphopcirclejerk', 'guitar', 'indieheads', 'edmproduction', 'vinyl', 'metal', 'radiohead', 'monstercat', 'headphones', 'metaljerk', 'audioengineering'}
    },
    {
        "name": "Soccer",
        "common_nodes": {"soccer", "fifa", "soccerstreams", "worldcup", "footballhighlights", "soccernerd"}
    },
    {
        "name": "Cars",
        "common_nodes": {'cars', 'teslamotors', 'justrolledintotheshop', 'mechanicadvice', 'subaru', 'shitty_car_mods', 'vandwellers', 'autos', 'jeep', 'bmw', 'autodetailing', 'carav', 'askcarsales', 'trucks', 'cartalk', 'whatcarshouldibuy', 'honda'}
    },
]


def find_definition(community: Set[Node]) -> Optional[CommunityDefinition]:
    best: Optional[CommunityDefinition] = None
    best_score = 0.35
    for definition in COMMUNITIES:
        c = sum(1 if node in community else 0 for node in definition["common_nodes"])
        percent = c / len(definition["common_nodes"])

        # The c / 20 term is arbitrary here, but tries to encourage higher count,
        #   so that a high count has a little bit of weight and the percent itself has the majority of the weight
        score = percent + c / 20
        if score > best_score:
            best = definition
            best_score = score
    return best


def combine_collapsed_graphs(graphs: List[nx.Graph]) -> nx.Graph:
    new_graph = nx.Graph()
    for graph in graphs:
        for u, v, data in graph.edges(data=True):
            existing_data = new_graph.get_edge_data(u, v)
            if existing_data is None:
                new_graph.add_edge(u, v, **data)
            else:
                new_graph.remove_edge(u, v)
                new_graph.add_edge(u, v, **{
                    **data,
                    **existing_data,
                    "weight": existing_data["weight"] + data["weight"]
                })

    return new_graph


def print_community(community_number: int, file, graph: nx.Graph, community: Set[Node]):
    MAX_DISPLAY = 3000
    # noinspection PyCallingNonCallable
    in_order = sorted(community, key=lambda node: graph.degree(node), reverse=True)
    more_string = "" if len(in_order) <= MAX_DISPLAY else f" and {len(in_order) - MAX_DISPLAY} more"
    best_definition = find_definition(community)
    name_string = f" ({best_definition['name']})" if best_definition is not None else ""
    print(f"Community {community_number}{name_string}: {in_order[:MAX_DISPLAY]}{more_string}", file=file)


def main():
    outputs_directory = Path("outputs")
    outputs_directory.mkdir(exist_ok=True)

    title_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-title.tsv"),
                                     Path(".cache/soc-redditHyperlinks-title.pickle"))
    body_graph = read_or_parse_file(Path(".downloads/soc-redditHyperlinks-body.tsv"),
                                    Path(".cache/soc-redditHyperlinks-body.pickle"))
    print("Collapsing graphs...")
    title_collapsed_graph = collapse(title_graph, contraction=contraction_weighted_on_keyword_similarity)
    body_collapsed_graph = collapse(body_graph, contraction=contraction_weighted_on_keyword_similarity)
    print("Done collapsing graphs.")

    print("Combining graphs and finding combined communities...")
    combined_graph = combine_collapsed_graphs([title_collapsed_graph, body_collapsed_graph])
    louvain_coms: List[Set[Node]] = nx.algorithms.community.louvain_communities(combined_graph)
    with open(Path("outputs", f"combined.txt"), 'w') as file:
        for i, community in enumerate(louvain_coms):
            if len(community) >= 20:
                print_community(i + 1, file, combined_graph, community)

    print("Found communities for combined graphs.")

    for name, graph, collapsed_graph in [
        ("title", title_graph, title_collapsed_graph),
        ("body", body_graph, body_collapsed_graph),
    ]:
        print()
        print(name)
        louvain_coms: List[Set[Node]] = nx.algorithms.community.louvain_communities(collapsed_graph)
        with open(Path("outputs", f"{name}.txt"), 'w') as file:
            for i, community in enumerate(louvain_coms):
                if len(community) >= 20:
                    print_community(i + 1, file, graph, community)


if __name__ == '__main__':
    main()
