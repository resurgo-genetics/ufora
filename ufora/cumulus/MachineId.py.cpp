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
#include "MachineId.hppml"

#include <stdint.h>
#include <boost/python.hpp>
#include "../core/python/ValueLikeCPPMLWrapper.hppml"
#include "../native/Registrar.hpp"
#include "../core/python/CPPMLWrapper.hpp"

using namespace Cumulus;

class MachineIdWrapper :
		public native::module::Exporter<MachineIdWrapper> {
public:
		std::string	     getModuleName(void)
			{
			return "Cumulus";
			}


		template<class T>
		static std::string simpleSerializer(const T& in)
			{
			ScopedPyThreads threads;

			return ::serialize<T>(in);
			}

		template<class T>
		static void simpleDeserializer(T& out, std::string inByteBlock)
			{
			ScopedPyThreads threads;

			out = ::deserialize<T>(inByteBlock);
			}

		void exportPythonWrapper()
			{
			using namespace boost::python;

			boost::python::object cls =
				ValueLikeCPPMLWrapper::exposeValueLikeCppmlType<MachineId>().class_()
					.def("__getstate__", simpleSerializer<MachineId>)
					.def("__setstate__", simpleDeserializer<MachineId>)
				;

			def("MachineId", cls);
			}
};

//explicitly instantiating the registration element causes the linker to need
//this file
template<>
char native::module::Exporter<MachineIdWrapper>::mEnforceRegistration =
		native::module::ExportRegistrar<
			MachineIdWrapper>::registerWrapper();




