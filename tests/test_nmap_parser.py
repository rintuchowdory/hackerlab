import unittest
from scripts.nmap_scan import parse_nmap_xml


SAMPLE = '''<?xml version="1.0"?>
<nmaprun><host><status state="up"/><address addr="127.0.0.1" addrtype="ipv4"/>
<ports><port protocol="tcp" portid="3000"><state state="open" reason="syn-ack"/>
<service name="http" product="Node.js" version="20"/></port></ports></host></nmaprun>'''


class NmapParserTests(unittest.TestCase):
    def test_parses_host_and_service(self):
        result = parse_nmap_xml(SAMPLE)
        self.assertEqual(result["hosts"][0]["addresses"], ["127.0.0.1"])
        self.assertEqual(result["hosts"][0]["ports"][0]["port"], 3000)
        self.assertEqual(result["hosts"][0]["ports"][0]["product"], "Node.js")


if __name__ == "__main__":
    unittest.main()
