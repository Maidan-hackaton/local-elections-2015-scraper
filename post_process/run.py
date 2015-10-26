#!/usr/bin/python
import json, os, csv

def parseJSON(filename):
    with open(filename) as f:
        item_list = json.load(f)
    return item_list

def writeJSON(list, filename):
    with open(filename, 'w') as f:
        json.dump(list, f)

def split_candidate_by_region(filename, dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    regions = {}
    for candidate in parseJSON(filename):
        region = candidate['region']
        if region not in regions:
            regions[region] = []
        regions[region].append(candidate)
    for region, candidates in regions.iteritems():
        writeJSON(candidates, os.path.join(dirname, 'city_council_candidates ' + region + u'.json'))

def candidates_to_csv(filename, dirname):
    csv_filename = os.path.join(dirname, '%s.csv')
    councils = {}
    candidates = parseJSON(filename)
    def full_council(region, council):
        return "%s, %s" % (region, council)
    for candidate in candidates:
        region = candidate['region']
        council = candidate['council']
        full_council_name = full_council(region, council)
        if full_council_name not in councils:
            councils[full_council_name] = []
        councils[full_council_name].append(candidate)
    for full_council_name, candidates in councils.iteritems():
        to_csv(candidates, csv_filename % full_council_name)

def to_csv(candidates, csv_filename):
    with open(csv_filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=candidates[0].keys())
        writer.writeheader()
        for candidate in sorted(candidates, cmp=lambda x, y: cmp(int(x['county_number']), int(y['county_number']))):
            writer.writerow({k:v.encode('utf8') for k,v in candidate.items()})

#split_candidate_by_region('data/city_council_candidates.json', 'data/by_region')
candidates_to_csv('data/city_council_candidates.json', 'data/csv/city_council_candidates')
