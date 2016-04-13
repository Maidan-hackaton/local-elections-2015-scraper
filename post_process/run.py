#!/usr/bin/python
# encoding=utf-8
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
        if 'council' in candidate:
            council = candidate['council']
        elif 'city_council' in candidate:
            council = candidate['city_council']
        else:
            council = u'Обласна рада'
        full_council_name = full_council(region, council)
        if full_council_name not in councils:
            councils[full_council_name] = []
        councils[full_council_name].append(candidate)
    for full_council_name, candidates in councils.iteritems():
        to_csv(candidates, csv_filename % full_council_name)

def to_csv(candidates, csv_filename):
    with open(csv_filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(candidates[0].keys()))
        writer.writeheader()
        if 'county_number' in candidates[0]:
            candidates = sorted(candidates, cmp=lambda x, y: cmp(int(x['county_number']), int(y['county_number'])))
        else:
            candidates = sorted(candidates, cmp=lambda x, y: cmp(x['full_name'], y['full_name']))
        for candidate in candidates:
            writer.writerow({k:v.encode('utf8') for k,v in candidate.items()})

#candidates_to_csv('data/city_council_candidates.json', 'data/csv/city_council_candidates')
#candidates_to_csv('data/region_council_candidates.json', 'data/csv/region_council_candidates')
candidates_to_csv('data/mayor_candidates.json', 'data/csv/mayor_candidates')
