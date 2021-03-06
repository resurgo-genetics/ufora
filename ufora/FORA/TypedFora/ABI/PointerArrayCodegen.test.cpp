/***************************************************************************
   Copyright 2015 Ufora Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
****************************************************************************/
#include "PointerArrayCodegen.hpp"
#include "NativeCodeCompilerTestFixture.hpp"

using namespace TypedFora::Abi;

class PointerArrayCodegenTestFixture : public NativeCodeCompilerTestFixture {
public:
	PointerArrayCodegenTestFixture()
		{
		}

	typedef PointerArray<long> table_type;

	typedef TypedNativeExpression<table_type*> table_ptr_expr;
};

BOOST_FIXTURE_TEST_SUITE( test_TypedFora_Abi_PointerArrayCodegen, PointerArrayCodegenTestFixture )

BOOST_AUTO_TEST_CASE( test_resizeExpression )
	{
	table_type table;

	compile(&table_ptr_expr::resize)(&table, 100);

	BOOST_CHECK(table.count() == 100);

	long aLong;
	table[10] = &aLong;

	BOOST_CHECK(compile(&table_ptr_expr::lookup)(&table, 10) == &aLong);

	//otherwise the pointer array will try to free it
	table[10] = 0;
	}

BOOST_AUTO_TEST_SUITE_END()


