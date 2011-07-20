%define api_version 1.6

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake16
Version:    %{api_version}.3
Release:    18%{?dist}.1
License:    GPLv2+ and MIT and OFSFDL
Group:      Development/Tools
Source:     ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Source10:   filter-provides-automake.sh
Source11:   filter-requires-automake.sh
URL:        http://sources.redhat.com/automake
Obsoletes:  automake = 1.6.3
# Required for tests:
Buildrequires:  autoconf >= 2.52
Buildrequires:  bison flex texinfo
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildArch:  noarch
Buildroot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1:     automake-pythondir-80994.patch
Patch2:     automake-1.6.3-info.patch
Patch3:     automake-1.6.3-man2-check.patch
Patch4:     automake-1.6.3-checks.patch
Patch5:     automake-1.6.3-CVE-2009-4029.patch

%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE10}
%define __find_requires %{SOURCE11}

# run "make check" by default
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%description
Automake is a tool for automatically generating
`Makefile.in' files compliant with the GNU Coding Standards.

This package contains Automake 1.6, an older version of Automake.
You should install it if you need to run automake in a project that
has not yet been updated to work with latest version of Automake.

%prep
%setup -q -n automake-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
rm -f automake.info*
mv automake.texi automake16.texi

%build
# use plain ./configure here to avoid overwriting config.{sub/guess}
./configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
   --bindir=%{_bindir} --datadir=%{_datadir} --libdir=%{_libdir}
make %{?_smp_mflags}

%check
%if ! %{_without_check}
  make check 
%endif

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

# create this dir empty so we can own it
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/aclocal

%post
/sbin/install-info %{_infodir}/automake16.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/automake16.info %{_infodir}/dir || :
fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_bindir}/*-%{api_version}
%exclude %{_bindir}/automake
%exclude %{_bindir}/aclocal
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
%dir %{_datadir}/aclocal
%{_infodir}/*

%changelog
* Tue Feb 16 2010 Karsten Hopp <karsten@redhat.com> 1.6.3-18.1
- fix CVE-2009-4029

* Fri Jul 31 2009 Karsten Hopp <karsten@redhat.com> 1.6.3-18
- rebuild

* Thu Jul 30 2009 Karsten Hopp <karsten@redhat.com> 1.6.3-17
- fix build problem

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 17 2007 Karsten Hopp <karsten@redhat.com> 1.6.3-14
- update licenses
- clarify BR autoconf for 'make check' only

* Tue Aug 28 2007 Karsten Hopp <karsten@redhat.com> 1.6.3-13
- fix license tag
- add missing patch (#225300)

* Tue Apr 03 2007 Karsten Hopp <karsten@redhat.com> 1.6.3-12
- buildrequire texinfo for makeinfo

* Thu Mar 22 2007 Karsten Hopp <karsten@redhat.com> 1.6.3-11
- more review fixes (#225300)

* Thu Mar 22 2007 Florian La Roche <laroche@redhat.com> 1.6.3-10
- change post/preun code to install info pages

* Tue Feb 20 2007 Karsten Hopp <karsten@redhat.com> 1.6.3-9
- merge review fixes

* Fri Jun 09 2006 Karsten Hopp <karsten@redhat.de> 1.6.3-8
- filter self provided dependencies

* Tue Jun 06 2006 Karsten Hopp <karsten@redhat.de> 1.6.3-7
- buildrequire flex for self tests

* Thu Jun 01 2006 Karsten Hopp <karsten@redhat.de> 1.6.3-6
- buildrequire bison for self tests

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep 28 2004 Warren Togami <wtogami@redhat.com> - 1.6.3-5
- trim docs

* Thu Sep 23 2004 Daniel Reed <djr@redhat.com> - 1.6.3-3
- rebuilt for dist-fc3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 14 2003 Jens Petersen <petersen@redhat.com> - 1.6.3-1
- New package based on automake-1.6.3 package
- conflicts with autoconf-1.6.3
- put info files in docs
- only ship versioned programs

* Mon Jan 27 2003 Jens Petersen <petersen@redhat.com> - 1.6.3-5
- patch from 1.7-branch to try python distutils for setting pythondir (#80994)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 1.6.3-3
- Fix unpackaged file

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com> 1.6.3-2
- add "--without check" rpmbuild option to switch "make check" off
- exclude info dir file
- don't gzip info files explicitly

* Mon Nov 18 2002 Jens Petersen <petersen@redhat.com>
- use api_version in version

* Mon Jul 29 2002 Jens Petersen <petersen@redhat.com> 1.6.3-1
- bug fix release 1.6.3

* Thu Jul 11 2002 Jens Petersen <petersen@redhat.com> 1.6.2-2
- add buildrequires autoconf 2.52 or greater [reported by Edward Avis]

* Wed Jun 19 2002 Jens Petersen <petersen@redhat.com> 1.6.2-1
- 1.6.2 (bug fix release)
- do "make check" after building

* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.6.1-2
- automated rebuild

* Tue Apr 23 2002 Jens Petersen <petersen@redhat.com> 1.6.1-1
- 1.6.1

* Tue Mar 12 2002 Jens Petersen <petersen@redhat.com> 1.6-1
- new package based on automake15
- 1.6

* Wed Jan 23 2002 Jens Petersen <petersen@redhat.com> 1.5-8
- better aclocal versioning

* Wed Jan 23 2002 Jens Petersen <petersen@redhat.com> 1.5-7
- don't version datadir/automake

* Tue Jan 15 2002 Jens Petersen <petersen@redhat.com> 1.5-6
- version suffix programs and data directories
- own symlinks to programs and /usr/share/aclocal

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.5-5
- automated rebuild

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-4
- Completely back out the fix for #56624 for now, it causes more problems
  than it fixes in either form.

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-3
- Don't use AS_DIRNAME, it doesn't work.

* Tue Jan  7 2002 Jens Petersen <petersen@redhat.com> 1.5-2
- Patch depout.m4 to handle makefiles passed to make with "-f" (#56624)

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-1
- Update to 1.5 - much better to coexist with autoconf 2.52...
- Fix specfile
- No patches

* Fri Aug 24 2001 Jens Petersen <petersen@redhat.com> - 1.4p5-2
- dont raise error when there is source in a subdirectory (bug #35156).
  This was preventing automake from working in binutuls/gas 
  [patch from HJ Lu <hjl@gnu.org>]
- format long lines of output properly with backslash + newlines as in 1.4
  (bug #35259) [patch from HJ Lu <hjl@gnu.org>]

* Sat Jul 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.4-p5, fixes #48788

* Tue Jun 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add the patch from #20559
- really update to 1.4-p4

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.4-p4

* Sat May 12 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.4-p1 to work with libtool-1.4

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #8870

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- revert to pristine automake-1.4.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)
