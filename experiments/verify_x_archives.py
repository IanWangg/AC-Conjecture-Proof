"""One-command hash, kernel, rotation-entry and strict-ledger replay."""
import argparse,base64,gzip,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for directory in (HERE.parent/'root',HERE.parent/'research_r'):
    sys.path.insert(0,str(directory))
from verify_vertex_voltage import verify
from elementary_verify import replay

p=argparse.ArgumentParser();p.add_argument('--certificates',required=True);p.add_argument('--directory',required=True);p.add_argument('--output',required=True)
args=p.parse_args();certs=Path(args.certificates);directory=Path(args.directory);directory.mkdir(parents=True,exist_ok=True)
manifest=json.loads((certs/'x_artifact_manifest.json').read_text());decoded={}
for row in manifest['transports']:
    encoded=(certs/row['file']).read_bytes();assert hashlib.sha256(encoded).hexdigest()==row['encoded_sha256']
    raw=gzip.decompress(base64.b64decode(encoded));assert hashlib.sha256(raw).hexdigest()==row['decoded_sha256']
    assert len(raw)==row['decoded_bytes'];decoded[row['file']]=raw
bundle=json.loads(decoded['x_second_phase_data.json.gz.b64']);names={
    'extensions':'x_extensions.json','affine_parameters':'x_parameters.json',
    'dual_obstructions':'x_duals.json','uniform_primitives':'x_primitives.json'}
for key,name in names.items():(directory/name).write_text(json.dumps(bundle[key])+'\n')
check_script=HERE/'verify_second_phase.py'
subprocess.run([sys.executable,str(check_script),str(certs/'v_vertex_identification_results.json'),
    *(str(directory/names[key]) for key in ('extensions','affine_parameters','dual_obstructions','uniform_primitives')),
    '--output',str(directory/'x_character_audit.json')],check=True)
rotations=json.loads(decoded['x_rotation_successors.json.gz.b64']);expected={(i,j) for i in range(7) for j in range(6)}
(directory/'x_rotation_successors.json').write_text(json.dumps(rotations)+'\n')
assert {tuple(r['rotation_offsets']) for r in rotations['records']}==expected
identifications=inequalities=0
initial=['xxxYYYY','xyxYXY']
for row in rotations['records']:
    i,j=row['rotation_offsets'];source=[initial[0][i:]+initial[0][:i],initial[1][j:]+initial[1][:j]]
    assert row['identification_data']['original_pair']==source
    audit=verify(row['identification_data'],row['cycle_certificates']);assert audit['status']=='PASS'
    identifications+=audit['vertex_identifications_independently_refolded'];inequalities+=audit['integer_potential_inequalities_checked']
entries=json.loads((certs/'x_all42_actual_entries.json').read_text());assert {tuple(r['rotation_offsets']) for r in entries}==expected
entry_moves=0
for row in entries:
    cert=row['certificate'];assert cert['start']==initial;i,j=row['rotation_offsets']
    assert cert['target']==[initial[0][i:]+initial[0][:i],initial[1][j:]+initial[1][:j]]
    entry_moves+=replay(cert)['moves']
walks=json.loads(decoded['x_barbell_walks.json.gz.b64']);strict_moves=0
(directory/'x_barbell_walks.json').write_text(json.dumps(walks)+'\n')
for row in walks['AK3_walks']:
    assert row['strict_certificate']['start']==initial
    strict_moves+=replay(row['strict_certificate'])['moves']
    (directory/(row['name']+'.strict.json')).write_text(json.dumps(row['strict_certificate'],indent=2)+'\n')
control=walks['AK2_control']['.full.json'];assert control['start']==['xxYYY','xyxYXY']
(directory/'x_barbell_ak2_full.json').write_text(json.dumps(control,indent=2)+'\n')
control_check=replay(control);assert control_check['endpoint']==['x','y']
assert replay(json.loads((certs/'x_h1_geometric_entry.json').read_text()))['endpoint']==['yXYXyx','yyyyXXX']
sources=decoded['x_h1_cap250_sources.jsonl.gz.b64'].decode().splitlines();assert len(sources)==985
(directory/'x_h1_cap250_sources.jsonl').write_bytes(decoded['x_h1_cap250_sources.jsonl.gz.b64'])
for source in sources:assert json.loads(source)['cyclic_energy']<=250
result={'status':'PASS','ordinary_AC_goal_solved':False,'hash_checked_transports':len(decoded),
    'character_audit':json.loads((directory/'x_character_audit.json').read_text()),
    'literal_rotation_successors':42,'vertex_identifications':identifications,
    'rotation_kernel_potential_inequalities':inequalities,'strict_rotation_entry_moves':entry_moves,
    'AK3_saved_walk_strict_moves':strict_moves,'AK2_full_control':control_check,
    'saved_H1_source_records':len(sources)}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
