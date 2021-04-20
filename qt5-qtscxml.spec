#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtscxml
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Scxml library
Summary(pl.UTF-8):	Biblioteka Qt5 Scxml
Name:		qt5-%{orgname}
Version:	5.15.2
Release:	2
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	5c52fd3e39707e46c6a37b4e13636ceb
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
BuildRequires:	qt5-doc-common >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Scxml library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Scxml.

%package -n Qt5Scxml
Summary:	The Qt5 Scxml library
Summary(pl.UTF-8):	Biblioteka Qt5 Scxml
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}

%description -n Qt5Scxml
Qt5 Scxml library.

%description -n Qt5Scxml -l pl.UTF-8
Biblioteka Qt5 Scxml.

%package -n Qt5Scxml-devel
Summary:	Qt5 Scxml - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Scxml - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Qml-devel >= %{qtdeclarative_ver}
Requires:	Qt5Scxml = %{version}-%{release}

%description -n Qt5Scxml-devel
Qt5 Scxml - development files.

%description -n Qt5Scxml-devel -l pl.UTF-8
Biblioteka Qt5 Scxml - pliki programistyczne.

%package doc
Summary:	Qt5 Scxml documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Scxml w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Scxml documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Scxml w formacie HTML.

%package doc-qch
Summary:	Qt5 Scxml documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Scxml w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Scxml documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Scxml w formacie QCH.

%package examples
Summary:	Qt5 Scxml examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Scxml
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Scxml examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Scxml.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# remove compiled examples (package only sources)
for d in $RPM_BUILD_ROOT%{_examplesdir}/qt5/scxml/* ; do
	[ -d "$d" ] && %{__rm} "$d/$(basename $d)"
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Scxml -p /sbin/ldconfig
%postun	-n Qt5Scxml -p /sbin/ldconfig

%files -n Qt5Scxml
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
# R: Qt5Core Qt5Qml
%attr(755,root,root) %{_libdir}/libQt5Scxml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Scxml.so.5
# R: Qt5Core
%attr(755,root,root) %{qt5dir}/bin/qscxmlc
%dir %{qt5dir}/qml/QtScxml
# R: Qt5Core Qt5Qml Qt5Scxml
%attr(755,root,root) %{qt5dir}/qml/QtScxml/libdeclarative_scxml.so
%{qt5dir}/qml/QtScxml/plugins.qmltypes
%{qt5dir}/qml/QtScxml/qmldir

%files -n Qt5Scxml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Scxml.so
%{_libdir}/libQt5Scxml.prl
%{_includedir}/qt5/QtScxml
%{_pkgconfigdir}/Qt5Scxml.pc
%{_libdir}/cmake/Qt5Scxml
%{qt5dir}/mkspecs/features/qscxmlc.prf
%{qt5dir}/mkspecs/modules/qt_lib_scxml.pri
%{qt5dir}/mkspecs/modules/qt_lib_scxml_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtscxml

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtscxml.qch
%endif

%files examples
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
%{_examplesdir}/qt5/scxml
