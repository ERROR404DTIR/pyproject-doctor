import tempfile,unittest
from pathlib import Path
import app
class AuditTests(unittest.TestCase):
 def test_missing_build(self):
  with tempfile.TemporaryDirectory() as d:
   r=app.audit({"project":{"name":"x"}},Path(d))
   self.assertGreater(r["warnings"],0)
if __name__=="__main__":unittest.main()
