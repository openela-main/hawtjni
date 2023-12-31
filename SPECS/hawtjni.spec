Name:             hawtjni
Version:          1.16
Release:          2%{?dist}
Summary:          Code generator that produces the JNI code
# Maven plugin is under ASL 2.0.
# stdint.h, shipped in JAR as resource, used only with M$ VC++, is under BSD.
# Everything else is under EPL-1.0
License:          ASL 2.0 and EPL-1.0 and BSD
URL:              http://hawtjni.fusesource.org/
BuildArch:        noarch

# That is the maven-release-plugin generated commit, but it's not tagged for some reason
# https://github.com/fusesource/hawtjni/issues/46
%global commit    fa1fd5dfdd0a1a5a67b61fa7d7ee7126b300c8f0
Source0:          https://github.com/fusesource/hawtjni/archive/%{commit}/hawtjni-%{commit}.tar.gz

BuildRequires:    maven-local
BuildRequires:    mvn(commons-cli:commons-cli)
BuildRequires:    mvn(org.apache.maven:maven-archiver)
BuildRequires:    mvn(org.apache.maven:maven-artifact)
BuildRequires:    mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:    mvn(org.apache.maven:maven-plugin-api)
BuildRequires:    mvn(org.apache.maven:maven-project)
BuildRequires:    mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:    mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:    mvn(org.apache.xbean:xbean-finder)
BuildRequires:    mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:    mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:    mvn(org.codehaus.plexus:plexus-io)
BuildRequires:    mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:    mvn(org.fusesource:fusesource-pom:pom:)
BuildRequires:    mvn(org.ow2.asm:asm)
BuildRequires:    mvn(org.ow2.asm:asm-commons)

Requires:         autoconf
Requires:         automake
Requires:         libtool
Requires:         make

%description
HawtJNI is a code generator that produces the JNI code needed to
implement java native methods. It is based on the jnigen code generator
that is part of the SWT Tools project which is used to generate all the
JNI code which powers the eclipse platform.

%package javadoc
Summary:          Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%package runtime
Summary:          HawtJNI Runtime

%description runtime
This package provides API that projects using HawtJNI should build
against.

%package -n maven-hawtjni-plugin
Summary:          Use HawtJNI from a maven plugin

%description -n maven-%{name}-plugin
This package allows to use HawtJNI from a maven plugin.

%prep
%setup -q -n hawtjni-%{commit}

%pom_disable_module hawtjni-example
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r :maven-eclipse-plugin

%mvn_package ":hawtjni-runtime" runtime
%mvn_package ":hawtjni-maven-plugin" maven-plugin

%mvn_alias :hawtjni-maven-plugin :maven-hawtjni-plugin

# javadoc generation fails due to strict doclint in JDK 8
%pom_remove_plugin :maven-javadoc-plugin hawtjni-runtime

%build
%mvn_build

%install
%mvn_install

%files runtime -f .mfiles-runtime
%doc readme.md license.txt changelog.md

%files -f .mfiles

%files javadoc -f .mfiles-javadoc
%doc license.txt

%files -n maven-hawtjni-plugin -f .mfiles-maven-plugin

%changelog
* Mon Jul  2 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.16-2
- Update license tag

* Mon Feb 26 2018 Michael Simacek <msimacek@redhat.com> - 1.16-1
- Update to upstream version 1.16

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Michael Simacek <msimacek@redhat.com> - 1.15-1
- Update to upstream version 1.15

* Mon Feb 13 2017 Michael Simacek <msimacek@redhat.com> - 1.10-9
- Add Requires on make

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1.10-8
- Regenerate BuildRequires

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-7
- Remove unneeded BR on maven-project-info-reports-plugin

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-4
- Remove maven-javadoc-plugin execution

* Fri Nov 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-3
- Spit runtime into subpackage
- Resolves: rhbz#1166607

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-2
- Add requires on autoconf, automake, libtool

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10-1
- Update to upstream version 1.10

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-4
- Migrate BuildRequires from junit4 to junit

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-3
- Remove BuildRequires on maven-surefire-provider-junit4

* Thu Mar  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-2
- Update to ASM4
- Resolves: rhbz#1073507

* Wed Sep 18 2013 Marek Goldmann <mgoldman@redhat.com> - 1.9-1
- Upstream release 1.9
- hawtjni: missing barriers in cache initialization, RHBZ#957181

* Tue Aug 06 2013 Marek Goldmann <mgoldman@redhat.com> - 1.8-3
- New guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Marek Goldmann <mgoldman@redhat.com> - 1.8-1
- Upstream release 1.8

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-5
- Remove unneeded BR: maven-idea-plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.6-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-2
- Replace asm2 requires with objectweb-asm
- Resolves: rhbz#902674

* Fri Sep 07 2012 gil cattaneo <puntogil@libero.it> 1.6-1
- Upstream release 1.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-3
- Remove eclipse plugin from BuildRequires

* Thu Jan 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-2
- Replace plexus-maven-plugin with plexus-containers implementation

* Sun Jan 15 2012 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Upstream release 1.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Marek Goldmann <mgoldman@redhat.com> 1.3-1
- Upstream release 1.3

* Fri Jul 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.2-1
- Upstream release 1.2
- Moved to new depmap macro

* Mon May 30 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-4
- Removed maven-shade-plugin dependency

* Mon May 30 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-3
- Split maven-hawtjni-plugin into new package
- Fixed license
- Fixed summary
- Using xz to compress source code

* Sun May 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-2
- Added maven-hawtjni-plugin

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-1
- Initial packaging
