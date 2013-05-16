Summary:	Automated theorem prover including linear arithmetic
Name:		alt-ergo
Version:	0.95.1
Release:	1
License:	CeCILL-C
Group:		Applications/Engineering
URL:		http://alt-ergo.lri.fr/
Source0:	http://alt-ergo.lri.fr/http/%{name}-%{version}/alt-ergo-%{version}.tar.gz
# Source0-md5:	c0f1cbfdae04f1c37853ed5fd10154ec
Source1:	%{name}.desktop
BuildRequires:	desktop-file-utils
BuildRequires:	gtksourceview2-devel
BuildRequires:	iconv
BuildRequires:	ocaml
BuildRequires:	ocaml-graph-devel
BuildRequires:	ocaml-lablgtk2-devel
BuildRequires:	ocaml-lablgtk2-gtksourceview2-devel
Requires(post):	coreutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Filter out symbols that are provided by interface files (*.mli) only.
# There are no corresponding symbols available at runtime.
%global __requires_exclude ocaml\\\(((Sig)|(Smt_ast)|(Why_ptree))\\\)

%description
Alt-Ergo is an automated theorem prover implemented in OCaml. It is
based on CC(X) - a congruence closure algorithm parameterized by an
equational theory X. This algorithm is reminiscent of the Shostak
algorithm. Currently CC(X) is instantiated by the theory of linear
arithmetics. Alt-Ergo also contains a home made SAT-solver and an
instantiation mechanism by which it fully supports quantifiers.

%package gui
Summary:	Graphical front end for alt-ergo
Group:		Applications/Engineering
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gtksourceview2

%description gui
A graphical front end for the alt-ergo theorem prover.

%prep
%setup -q

# Set print_flag to false or invoking with -select
# from "why" will pause every invocation :-(.
sed -i -e 's/let print_flag = true/let print_flag = false/;' pruning.ml

%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_datadir} \
	--mandir=%{_mandir}

%{__make} OCAMLBEST=opt OCAMLOPT=ocamlopt.opt
%{__make} OCAMLBEST=opt OCAMLOPT=ocamlopt.opt gui

iconv -f ISO-8859-1 -t UTF-8 -o CeCILL-C.utf8 CeCILL-C
touch -r CeCILL-C CeCILL-C.utf8
%{__mv} -f CeCILL-C.utf8 CeCILL-C

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir}}

%{__make} install \
	OCAMLBEST=opt OCAMLOPT=ocamlopt.opt \
	DESTDIR=$RPM_BUILD_ROOT

# Remove files we do not want installed
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/*.{cmx,o}

# Install the desktop file
desktop-file-install --dir $RPM_BUILD_ROOT%{_desktopdir} %{SOURCE1}

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_desktop_database

%postun gui
%update_desktop_database

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}/
%{_mandir}/man1/alt-ergo.1.*
%doc COPYING CeCILL-C CHANGES

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/altgr-ergo
%{_desktopdir}/%{name}.desktop
%{_datadir}/gtksourceview-2.0/language-specs/%{name}.lang
