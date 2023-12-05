from pathlib import Path
from typing import List, Set, Dict, Tuple

import networkx as nx
import itertools

from matplotlib import pyplot as plt

from community_conflict import Node
from community_conflict.cache import read_or_parse_file
from community_conflict.collapse import collapse, contraction_weighted_on_keyword_similarity
from community_conflict.community import combine_collapsed_graphs, find_community, print_community, CommunityDefinition, \
    ALL_COMMUNITY_DEFINITIONS, find_definition

EMPTY_DICT = dict()

POLITICAL_COMMUNITY_DEFINITIONS: List[CommunityDefinition] = [
    {
        "name": "Miscellaneous",
        "common_nodes": {'technology', 'futurology', 'documentaries', 'truereddit', 'collapse', 'basicincome', 'environment'}
    },
    {
        "name": "Conspiracy",
        "common_nodes": {'conspiracy', 'topmindsofreddit', 'undelete', 'conspiratard', 'oppression', 'politic', 'wikileaks', 'privacy', 'c_s_t', 'redditcensorship', 'nolibswatch', 'targetedenergyweapons', 'darkenlightenment'}
    },
    {
        "name": "Religion",
        "common_nodes": {'atheism', 'changemyview', 'badphilosophy', 'christianity', 'philosophy', 'badhistory', 'islam', 'circlejerkcopypasta', 'exmuslim', 'askphilosophy', 'catholicism', 'badsocialscience', 'agitation', 'badscience', 'judaism', 'debatereligion', 'truechristian', 'bad_religion', 'religion'}
    },
    {
        "name": "Politics (Left)",
        "common_nodes": {'politics', 'news', 'shitliberalssay', 'libertarian', 'shitstatistssay', 'enoughtrumpspam', 'politicaldiscussion', 'shitpoliticssays', 'badeconomics', 'panichistory', 'badpolitics'}
    },
    {
        "name": "Drama",
        "common_nodes": {'subredditdrama', 'subredditcancer', 'kotakuinaction', 'mensrights', 'srssucks', 'tumblrinaction', 'bestofoutrageculture', 'gamerghazi', 'thepopcornstand', 'theoryofreddit', 'blackout2015', 'againstmensrights', 'negareddit', 'feminism'}
    },
    {
        "name": "Democrats",
        "common_nodes": {'sandersforpresident', 'political_revolution', 'enough_sanders_spam', 'wayofthebern', 'gmomyths', 'hillaryforprison', 'jillstein', 'grassrootsselect', 'kossacks_for_sanders', 'dncleaks', 'democrats', 'therecordcorrected', 'enoughhillhate'}
    },
    {
        "name": "Race",
        "common_nodes": {'blackladies', 'blackfellas', 'starterpacks', 'indiana', 'indianapolis', 'blackpower', 'bloomington', 'justproblackthings', 'blackgirls', 'raldi', 'discusstheopenletter', 'trueblackculture', 'anarchisme', 'indianauniversity'}
    },
    {
        "name": "Not United States",
        "common_nodes": {'unitedkingdom', 'ukpolitics', 'vexillology', 'scotland', 'gulag', 'mhocgevotes', 'labouruk', 'ukipparty', 'glasgow', 'badukpolitics', 'britishpolitics', 'radicalfeminism', 'labour', 'bristol', 'wales', 'freyaslight', 'vexillologycirclejerk', 'voting'}
    },
    {
        "name": "Something 1",
        "common_nodes": {'drama', 'canada', 'metacanada', 'canadapolitics', 'vancouver', 'trueredditdrama', 'quebec', 'circlejerkaustralia', 'freespeech', 'kreiswichs', 'torontoanarchy', 'alberta'}
    },
    {
        "name": "World News",
        "common_nodes": {'worldnews', 'europe', 'shitamericanssay', 'dataisbeautiful', 'circlebroke2', 'de', 'france', 'mapporn', 'circlebroke', 'australia', 'sweden', 'thenetherlands', 'russia', 'italy', 'murica', 'polandball', 'iranian', 'germany', 'brasil', 'romania', 'denmark', 'turkey', 'portugal', 'mexico', 'argentina', 'iran', 'belgium'}
    },
    {
        "name": "History",
        "common_nodes": {'askhistorians', 'history', 'depthhub', 'syriancivilwar', 'geopolitics', 'historyporn', 'shitwehraboossay', 'asksocialscience', 'anythinggoesnews', 'neutralpolitics', 'postnationalist', 'propagandaposters', 'indiancountry', 'combatfootage', 'militaryporn', 'alternativehistory', 'warthunder', 'historynetwork'}
    },
    {
        "name": "Middle East",
        "common_nodes": {'india', 'israel', 'arabs', 'pakistan', 'indianews', 'bakchodi', 'palestine', 'hinduism', 'abcdesis', 'indiaspeaks', 'sikh', 'indiadiscussion', 'saudiarabia', 'indiamain', 'israelpalestine', 'bangladesh', 'indianpeoplefacebook', 'bangalore', 'indianleft', 'israelexposed', 'kuwait'}
    },
    {
        "name": "Conservative",
        "common_nodes": {'the_donald', 'worldpolitics', 'european', 'conservative', 'againsthatesubreddits', 'worstof', 'asablackman', 'uncensorednews', 'altright', 'whiterights', 'debatefascism', 'shitrconservativesays', 'fuckthealtright', 'republican', 'censorship', 'internethitlers', 'antisemitismwatch', 'pussypass', 'askthe_donald', 'marchagainsttrump', 'bannedfromthe_donald', 'nationalsocialism', 'physical_removal', 'iamnotracistbut', 'trendingreddits', 'unpopularopinion', 'mr_trump', 'offensivespeech', 'shitthe_donaldsays', 'hatesubsinaction', 'askaconservative', 'conservatives', 'edefreiheit', 'europeannationalism', 'debatealtright'}
    },
    {
        "name": "Ideologies",
        "common_nodes": {'anarcho_capitalism', 'socialism', 'anarchism', 'enoughlibertarianspam', 'latestagecapitalism', 'fullcommunism', 'economics', 'communism', 'debateanarchism', 'enoughcommiespam', 'capitalismvsocialism', 'banned', 'goldandblack', 'shittydebatecommunism', 'metanarchism', 'shittankiessay', 'completeanarchy', 'praxacceptance', 'anarchismonline', 'communism101', 'debatecommunism', 'anarchy101', 'leftwithsharpedge', 'historyofideas', 'debateacommunist', 'anticonsumption', 'racism', 'killthosewhodisagree', 'education', 'anarchistnews', 'nonfictionbookclub', 'evolutionreddit', 'chomsky', 'shitsocialismsays'}
    },
]


def show_conflicts_negative_percentage_graph(conflicts: List[Tuple[int, int, str, str]]):
    labels = []
    negative_percentages = []
    for positive_links, negative_links, a, b in sorted(conflicts, key=lambda conflict: conflict[1] / max(1, conflict[0] + conflict[1]), reverse=True):
        total_links = positive_links + negative_links
        if total_links > 200:
            negative_percent = negative_links / total_links
            print(f"Conflicts with source:  {a:<20} and target  {b:<20} : {negative_percent * 100.0:.2f}% with positive: {positive_links:<6} and negative: {negative_links:<6}")
            labels.append(f"{a} to {b}")
            negative_percentages.append(negative_percent * 100.0)

    fig, ax = plt.subplots()
    ax.bar(labels, negative_percentages, color='red')
    ax.set_ylabel('Negative Percentage')
    ax.set_xlabel('Source to Target')
    ax.set_title('Negative Percentage for Conflicts')

    plt.xticks(rotation=45, ha='right')

    plt.show()


def show_conflicts_negative_count_graph(conflicts: List[Tuple[int, int, str, str]]):
    labels = []
    negative_link_counts = []
    total_link_counts = []
    for positive_links, negative_links, a, b in sorted(conflicts, key=lambda conflict: conflict[1], reverse=True):
        total_links = positive_links + negative_links
        if total_links > 200:
            labels.append(f"{a} to {b}")
            negative_link_counts.append(negative_links)
            total_link_counts.append(total_links)

    bar_width = 0.35

    fig, ax = plt.subplots()
    ax.bar(range(len(negative_link_counts)), negative_link_counts, bar_width, color='red', label='Negative Links')
    ax.bar([i + bar_width for i in range(len(negative_link_counts))], total_link_counts, bar_width, color='blue', label='Total Links')

    ax.set_ylabel('Negative Links')
    ax.set_xlabel('Source to Target')
    ax.set_title('Negative Links for Conflicts')
    ax.set_xticks([i + bar_width / 2 for i in range(len(negative_link_counts))])
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    plt.show()



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
    political_nodes_count_dict: Dict[Node, int] = dict()
    for _ in range(10):
        louvain_coms: List[Set[Node]] = nx.algorithms.community.louvain_communities(combined_graph)

        political_community = find_community("Political", louvain_coms, ALL_COMMUNITY_DEFINITIONS)
        if political_community is not None:
            for node in political_community:
                political_nodes_count_dict[node] = (political_nodes_count_dict.get(node) or 0) + 1

    political_nodes = set(node for node, count in political_nodes_count_dict.items() if count >= 6)

    assert len(political_nodes) > 5000, f"We expect this value to be very large. Even bigger than whatever is it now. political_nodes: {political_nodes}"
    print(political_nodes)
    print(len(political_nodes))

    simple_political_graph = combined_graph.subgraph(political_nodes)
    political_communities: List[Set[Node]] = nx.algorithms.community.louvain_communities(simple_political_graph)

    with open(Path(outputs_directory, "political.txt"), 'w') as file:
        for i, community in enumerate(political_communities):
            print_community(i + 1, file, simple_political_graph, community, POLITICAL_COMMUNITY_DEFINITIONS)

    # focus_list = ["History", "Politics (Left)", "Race", "Ideologies", "Conspiracy", "Democrats", "Conservative"]
    focus_communities: List[Tuple[CommunityDefinition, Set[Node]]] = []
    for community in political_communities:
        definition = find_definition(community, POLITICAL_COMMUNITY_DEFINITIONS)
        # if definition is not None and definition["name"] in focus_list:
        if definition is not None:
            pair = (definition, community)
            focus_communities.append(pair)

    conflicts: List[Tuple[int, int, str, str]] = []
    # now detect conflict between communities
    for (a_definition, a), (b_definition, b) in itertools.product(focus_communities, focus_communities):
        if a_definition == b_definition:
            continue
        positive_links = 0
        negative_links = 0
        for a_node, b_node in itertools.product(a, b):
            title_edge_data_dict = title_graph.get_edge_data(a_node, b_node) or EMPTY_DICT
            body_edge_data_dict = body_graph.get_edge_data(a_node, b_node) or EMPTY_DICT
            for edge_data in title_edge_data_dict.values():
                if edge_data["link_sentiment"] == 1:
                    positive_links += 1
                else:
                    negative_links += 1
            for edge_data in body_edge_data_dict.values():
                if edge_data["link_sentiment"] == 1:
                    positive_links += 1
                else:
                    negative_links += 1

        conflicts.append((positive_links, negative_links, a_definition['name'], b_definition['name']))

    show_conflicts_negative_percentage_graph(conflicts)
    show_conflicts_negative_count_graph(conflicts)



if __name__ == '__main__':
    main()