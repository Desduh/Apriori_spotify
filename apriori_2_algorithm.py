# A simple 1-level association rule apriori
# algorithm implementation
#
# Author: Fabrício G. M. de Carvalho, Ph.D

itemset = ["alternative", "alternative rock", "college rock", "experimental rock", "goth rock", "grunge", "hardcore punk", "hard rock", "indie rock", "new wave", "progressive rock", "punk", "shoegaze", "steampunk", "anime", "blues", "acoustic blues", "chicago blues", "classic blues", "contemporary blues", "country blues", "delta blues", "electric blues", "children's music", "lullabies", "sing-along", "stories", "classical", "avant-garde", "baroque", "chamber music", "chant", "choral", "classical crossover", "early music", "high classical", "impressionist", "medieval", "minimalism", "modern composition", "opera", "orchestral", "renaissance", "romantic", "wedding music", "comedy", "novelty", "country", "alternative country", "americana", "bluegrass", "contemporary bluegrass", "contemporary country", "country gospel", "honky tonk", "outlaw country", "traditional bluegrass", "traditional country", "urban cowboy", "dance / emd", "breakbeat", "dubstep", "exercise", "garage", "hardcore", "hard dance", "hi-nrg / eurodance", "house", "jackin house", "jungle/drum'n'bass", "techno", "trance", "disney", "easy listening", "bop", "lounge", "swing", "electronic", "ambient", "crunk", "downtempo", "electro", "electronica", "electronic rock", "idm/experimental", "industrial", "enka", "french pop", "german folk", "german pop", "fitness & workout", "hip-hop/rap", "alternative rap", "bounce", "dirty south", "east coast rap", "gangsta rap", "hardcore rap", "hip-hop", "latin rap", "old school rap", "rap", "underground rap", "west coast rap", "holiday", "chanukah", "christmas", "christmas: children's", "christmas: classic", "christmas: classical", "christmas: jazz", "christmas: modern", "christmas: pop", "christmas: r&b", "christmas: religious", "christmas: rock", "easter", "halloween", "holiday: other", "thanksgiving", "indie pop", "industrial", "inspirational - christian & gospel", "ccm", "christian metal", "christian pop", "christian rap", "christian rock", "classic christian", "contemporary gospel", "gospel", "christian & gospel", "praise & worship", "qawwali", "southern gospel", "traditional gospel", "instrumental", "march (marching band)", "j-pop", "j-rock", "j-synth", "j-ska", "j-punk", "jazz", "acid jazz", "avant-garde jazz", "big band", "blue note", "contemporary jazz", "cool", "crossover jazz", "dixieland", "ethio-jazz", "fusion", "hard bop", "latin jazz", "mainstream jazz", "ragtime", "smooth jazz", "trad jazz", "k-pop", "karaoke", "kayokyoku", "latino", "alternativo & rock latino", "baladas y boleros", "brazilian", "contemporary latin", "latin jazz", "pop latino", "raíces", "reggaeton y hip-hop", "regional mexicano", "salsa y tropical", "new age", "environmental", "healing", "meditation", "nature", "relaxation", "travel", "opera", "pop", "adult contemporary", "britpop", "pop/rock", "soft rock", "teen pop", "r&b/soul", "contemporary r&b", "disco", "doo wop", "funk", "motown", "neo-soul", "quiet storm", "soul", "reggae", "dancehall", "dub", "roots reggae", "ska", "rock", "adult alternative", "american trad rock", "arena rock", "blues-rock", "british invasion", "death metal/black metal", "glam rock", "hair metal", "hard rock", "metal", "jam bands", "prog-rock/art rock", "psychedelic", "rock & roll", "rockabilly", "roots rock", "singer/songwriter", "southern rock", "surf", "tex-mex", "singer/songwriter", "alternative folk", "contemporary folk", "contemporary singer/songwriter", "folk-rock", "new acoustic", "traditional folk", "soundtrack", "foreign cinema", "musicals", "original score", "soundtrack", "tv soundtrack", "spoken word", "tex-mex / tejano", "chicano", "classic", "conjunto", "conjunto progressive", "new mex", "tex-mex", "vocal", "barbershop", "doo-wop", "standards", "traditional pop", "vocal jazz", "vocal pop"]
import csv

def extract_artist_genres_from_csv(filename):
    transactions_bd = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho do arquivo CSV
        for row in reader:
            artist_genres = eval(row[2])  # Índice 2 representa a coluna 'artist_genres'
            if artist_genres:
                transactions_bd.append(set(artist_genres))
    return transactions_bd

# Exemplo de uso
filename = 'artists.csv'
transactions_bd = extract_artist_genres_from_csv(filename)


#Support calculation
def support(Ix, Iy, bd):
    sup = 0
    for transaction in bd:
        if (Ix.union(Iy)).issubset(transaction):
            sup+=1
    sup = sup/len(bd)
    return sup

# Confidence calculation
def confidence(Ix, Iy, bd):
    Ix_count = 0
    Ixy_count = 0
    for transaction in bd:
        if Ix.issubset(transaction):
            Ix_count+=1
            if (Ix.union(Iy)).issubset(transaction):
                Ixy_count += 1
    conf = Ixy_count / Ix_count
    return conf
            

# This function eliminates all the items in 
# ass_rules which have sup < min_sup and
# conf < min_conf. It returns a "pruned" list
def prune(ass_rules, min_sup, min_conf):
    pruned_ass_rules = []
    for ar in ass_rules:
        if ar['support'] >= min_sup and ar['confidence'] >= min_conf:
            pruned_ass_rules.append(ar)
    return pruned_ass_rules
    

# Apriori for association between 2 items
def apriori_2(itemset, bd, min_sup, min_conf):
    ass_rules = []
    ass_rules.append([]) #level 1 (large itemsets)
    for item in itemset:
        sup = support({item},{item},bd)
        ass_rules[0].append({'rule': str(item), \
                             'support':sup, \
                             'confidence': 1})        
    ass_rules[0] = prune(ass_rules[0],min_sup, min_conf)
    ass_rules.append([]) #level 2 (2 items association)
    for item_1 in ass_rules[0]:
        for item_2 in ass_rules[0]:
            if item_1['rule'] != item_2['rule']:
                rule = item_1['rule']+' , '+item_2['rule']
                Ix = {item_1['rule']}
                Iy = {item_2['rule']}
                sup = support(Ix,Iy, bd)
                conf = confidence(Ix, Iy, bd)
                ass_rules[1].append({'rule':rule, \
                                     'support': sup, \
                                     'confidence': conf})
    ass_rules[1] = prune(ass_rules[1],min_sup, min_conf)
    return ass_rules

    

print(apriori_2(itemset, transactions_bd, 0.001, 0.7))
cont = input('Press enter to continue...')



    
