#   Copyright 2015 Ufora Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import unittest

import ufora.FORA.python.Runtime as Runtime

class AxiomsTest(unittest.TestCase):
    def testAxiomLookups(self):
        axioms = Runtime.getMainRuntime().getAxioms()

        jmtsToTest = [axiom.signature() for axiom in axioms]

        for tupJmt in jmtsToTest:
            linear = axioms.axiomSearchLinear(tupJmt)
            tree = axioms.axiomSearchTree(tupJmt)
            self.assertEqual(
                linear,
                tree,
                "Didn't produce same results for %s: %s vs %s" % (str(tupJmt), linear, tree)
                )

    def testAxiomLookupsDontThrow(self):
        axioms = Runtime.getMainRuntime().getAxioms()

        jmtsToTest = [axiom.signature() for axiom in axioms]

        for tupJmt in jmtsToTest:
            tree = axioms.axiomSearchTree(tupJmt)
            
