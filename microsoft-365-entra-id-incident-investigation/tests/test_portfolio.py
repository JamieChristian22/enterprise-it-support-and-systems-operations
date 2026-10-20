"""Offline repository quality gates: no credentials or tenant access required."""
import pathlib,re,unittest,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
class PortfolioQuality(unittest.TestCase):
 def test_required_artifacts(self):
  for f in ['README.md','docs/INC-2026-1042.md','docs/ESCALATION_AND_SLA.md','docs/ROOT_CAUSE_DECISION_TREE.md','docs/PRIVACY_AND_PUBLICATION.md','scripts/GraphDiagnostics.Core.psm1','tests/GraphDiagnostics.Tests.ps1']:
   with self.subTest(f=f): self.assertTrue((ROOT/f).is_file())
 def test_evidence_count(self):
  self.assertEqual(len(list((ROOT/'evidence/screenshots').glob('*.png'))),10)
 def test_no_secrets_in_text(self):
  bad=[r'(?i)client_secret\s*[:=]\s*["\x27]?\w{8,}',r'(?i)-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',r'(?i)password\s*[:=]\s*["\x27][^"\x27]{8,}']
  for f in ROOT.rglob('*'):
   if f.suffix not in ('.md','.ps1','.psm1','.py','.yml','.yaml','.json','.csv','.mmd'): continue
   t=f.read_text(encoding='utf-8')
   for pat in bad:
    with self.subTest(f=str(f),pat=pat): self.assertIsNone(re.search(pat,t))
 def test_no_real_personal_identifiers_in_text(self):
  for f in ROOT.rglob('*'):
   if f.suffix not in ('.md','.ps1','.psm1','.py','.yml','.yaml','.json','.csv','.mmd'): continue
   t=f.read_text(encoding='utf-8').lower()
   if f.name == 'test_portfolio.py': continue  # patterns in this test are not leaked evidence
   self.assertNotIn('jamie.christian2@yahoo.com',t,str(f))
   self.assertNotIn('/users/jamiechristian',t,str(f))
 def test_simulation_disclosure(self):
  for f in ['README.md','docs/INC-2026-1042.md']:
   self.assertIn('simulat',(ROOT/f).read_text().lower())
if __name__=='__main__': unittest.main()
