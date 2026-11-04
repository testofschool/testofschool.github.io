#!/usr/bin/env python3
"""Guard the accepted content order; visual prominence still requires a render review."""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import json
import sys
import subprocess
import tempfile

class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children, self.words = [], []
    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()
    def text(self):
        return ' '.join(self.words + [c.text() for c in self.children])
    def has_class(self, cls):
        return cls in self.attrs.get('class', '').split()

class Page(HTMLParser):
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
    def __init__(self, source):
        super().__init__(); self.root = Node('document', []); self.stack = [self.root]; self.feed(source)
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.stack[-1]); self.stack[-1].children.append(n)
        if tag not in self.VOID: self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]; break
    def handle_data(self, data):
        self.stack[-1].words.append(data)

def check(root):
    issues=[]; pages=[]
    contract=json.loads((root/'portfolio-contract.json').read_text())
    for rel in ['kr/index.html', 'index.html']:
        p=root/rel
        if not p.is_file(): issues.append(f'{rel}: page missing'); continue
        page=Page(p.read_text()); nodes=list(page.root.walk())
        main=next((n for n in nodes if n.tag=='main'), None)
        if main is None: issues.append(f'{rel}: main missing'); continue
        sections=[n for n in main.children if n.tag in ('section','article')]
        order=[next((c for c in contract['required_order'] if n.has_class(c)), 'other') for n in sections]
        projected=[c for c in order if c!='other']
        if projected!=contract['required_order'] or not order or order[0]!='samil':
            issues.append(f'{rel}: accepted main/support order changed: {order}')
        samil=next((n for n in sections if n.has_class('samil')),None)
        if samil:
            ns=list(samil.walk()); headline=' '.join(n.text() for n in ns if n.tag in ('h1','h2'))
            expected=['삼일PwC','본선 진출'] if rel.startswith('kr') else ['Samil PwC','Finalist']
            if not all(s in headline for s in expected): issues.append(f'{rel}: Samil finalist headline missing')
            imgs=[n for n in ns if n.tag=='img' and '/samil-finalist-' in n.attrs.get('src','')]
            if not imgs: issues.append(f'{rel}: actual Samil badge missing from main proof')
            for n in imgs:
                if not (root/n.attrs['src'].lstrip('/')).is_file(): issues.append(f'{rel}: badge asset missing')
            forbidden=['Everdict','후속','피드백','회귀 테스트','regression test']
            if any(x.lower() in samil.text().lower() for x in forbidden): issues.append(f'{rel}: Samil claim expanded beyond approved finalist fact')
        research=next((n for n in sections if n.has_class('research')),None)
        if not research: issues.append(f'{rel}: research support removed')
        else:
            label=' '.join(n.text() for n in research.walk() if n.tag in ('h1','h2') or n.has_class('accepted'))
            scope=['NeurIPS 2026','워크숍','포스터 채택'] if rel.startswith('kr') else ['NeurIPS 2026','Workshop','poster accepted']
            if not all(x in label for x in scope): issues.append(f'{rel}: research acceptance scope changed')
        if contract.get('version', 1) >= 2:
            for cls, required in {
                'execution': ['50팀', '4,200여 명', '규정다름'] if rel.startswith('kr') else ['50 finalist teams', '4,200 participants', 'Gyujeong Dareum'],
                'community': ['블룸 가드너', 'AI Tinkerers Seoul', '챕터 운영 지원'] if rel.startswith('kr') else ['Bloom Gardener', 'AI Tinkerers Seoul', 'Supporting the Seoul chapter'],
                'collaboration': (['참여 중', '해커톤·공모전'] if rel.startswith('kr') else ['Participating', 'Hackathons & competitions']) if contract.get('version', 1) >= 4 else (['참여 중', '데이터', '음향'] if rel.startswith('kr') else ['In progress', 'Data', 'audio']),
            }.items():
                section=next((n for n in sections if n.has_class(cls)),None)
                if section is None or not all(s in section.text() for s in required):
                    issues.append(f'{rel}: {cls} required result/role scope missing')
            execution=next((n for n in sections if n.has_class('execution')),None)
            if execution and not any(n.tag=='img' and 'mabc-finalist.webp' in n.attrs.get('src','') for n in execution.walk()):
                issues.append(f'{rel}: original MABC certificate missing')
            if contract.get('execution_visibility_revision') and execution:
                output=next((n for n in execution.walk() if n.tag=='img' and 'mabc-service-sample.jpg' in n.attrs.get('src','')),None)
                if output is None:
                    issues.append(f'{rel}: actual MABC output missing')
                else:
                    ancestor=output.parent
                    disclosure=None
                    while ancestor is not None:
                        if ancestor.tag=='details':
                            disclosure=ancestor
                            break
                        ancestor=ancestor.parent
                    collapsed=contract['execution_visibility_revision']['actual_service_output'].startswith('collapsed')
                    if collapsed and (disclosure is None or 'open' in disclosure.attrs):
                        issues.append(f'{rel}: actual MABC output must be collapsed by default')
                    elif not collapsed and disclosure is not None:
                        issues.append(f'{rel}: actual MABC output must be visible without expanding a disclosure')
        if contract.get('version', 1) >= 4:
            activities={n.attrs.get('data-activity'):n for n in nodes if n.tag=='li' and n.attrs.get('data-activity')}
            expected=contract['ongoing_activity_revision']['entries']
            if list(activities)!=[entry['id'] for entry in expected]:
                issues.append(f'{rel}: confirmed current activity inventory changed')
            for entry in expected:
                item=activities.get(entry['id'])
                if item is None: continue
                state=entry['status_ko' if rel.startswith('kr') else 'status_en']
                if state not in item.text() or not any(n.tag=='a' and n.attrs.get('href')==entry['href'] for n in item.walk()):
                    issues.append(f'{rel}: {entry["id"]} current state/source missing')
        if not any(n.tag=='a' and n.has_class('contact-button') and n.attrs.get('href')=='mailto:gangjeongmin23@gmail.com' for n in nodes):
            issues.append(f'{rel}: interview contact path missing')
        pages.append({'file':rel,'observed_order':order})
    return {'status':'FAIL' if issues else 'PASS','scope':'Structural/content guard; not visual acceptance, deployment or hiring proof.','pages':pages,'issues':issues}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--staged',action='store_true');args=parser.parse_args()
    try:
        if args.staged:
            with tempfile.TemporaryDirectory(prefix='portfolio-index-') as tmp:
                subprocess.run(['git','checkout-index','--all','--prefix',tmp+'/'],cwd=args.root,check=True,capture_output=True)
                result=check(Path(tmp))
                result['input']='git index snapshot, not unstaged working tree'
        else: result=check(args.root)
    except (OSError, ValueError, subprocess.CalledProcessError) as e: result={'status':'FAIL','issues':[str(e)]}
    print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['status']=='PASS' else 1)
