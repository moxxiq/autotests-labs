% ******* ���� ��� ��������� ��������� �� ���� 3008-95 ********
% ***** ������: ������ �. �., ��������� �. �., ������ �. �. ****

% 1. ������������ ����
\ProvidesClass{dstu}[2015/12/16 v1.0 ���� ��� ��������� ��������� �� ���� 3008-95]
\NeedsTeXFormat{LaTeX2e} % �������� ������

% 2. ����������� "����������� ����"
\LoadClass[a4paper,14pt,ukrainian,oneside]{extreport}


% 3. ����������� ������
% ����� ������
\RequirePackage{cmap}% ��� ��������� ������ � pdf
\RequirePackage[T2A]{fontenc} % ����� ��� �������� ��������� ������
\RequirePackage[cp1251]{inputenc} % ����� ��� �������� Windows'�������� ��������� cp1251
\RequirePackage[russian,ukrainian]{babel} % ����� ��� �������� ��������� �� �������� ���
\RequirePackage{pscyr} % ����� �� ������� ���������� ��������
\RequirePackage{mathtext} % ������� ������� � ����� ������������ ������
\RequirePackage{amssymb,amsfonts,amsmath,amsthm} % ������� ������� � ����� ������������ ������
\RequirePackage{textcomp} % ������� ������� � ����� ������������ ������
\RequirePackage{upgreek} % ����� ��� ������ �������� ����

% �������� ������
\RequirePackage{graphicx} % �������� ����� ��� ������� �������
\RequirePackage{subfig} % ����� ��� ������� ���������
\RequirePackage{flafter} % ����� �������, �� ������� �� ������� ������ �� �'�������� ������ ��������� �� ����� ����
\RequirePackage{caption} % ����� ��� ������������� ��������� ������� �� �������
\RequirePackage{xtab} % ����� ��� ������ �������
\RequirePackage{longtable} % ����� ��� ������ �������
\RequirePackage{multirow} % ����� ��� ��'������� ����� �������
\RequirePackage{array} % ����� ��� ����������� ��������� �������

% ������ ��� ������������ ������� �� ����
\RequirePackage[includehead, headsep=0pt, footskip=0pt, top=2cm, bottom=2cm, left=2cm, right=1cm]{geometry} % ������ ���� �������
\RequirePackage{indentfirst} % ������ ��� ������� ����� ������
\RequirePackage{hanging} % ������ ��� ��� ����� ����� ������
\RequirePackage[shortlabels]{enumitem}	% ����� ��� ������������ ������
\RequirePackage{setspace}	% ����� ��� ����, ��� ����� ���� ������ ���������� ��������
\RequirePackage{fancyhdr} % ����� �������� ��� ����������� ������� ������ �������
\RequirePackage{etoolbox} % ����� ��� ���������� �������� ������� � ���������� �� ������������ ������� �������� �� �����������

% ���� ��������� �� �����
\RequirePackage[rm,small,raggedright]{titlesec} % ����� ��� ������� ��������� ������ ���������
\RequirePackage[titles,subfigure]{tocloft} % ����� ��� ������� ��������� ������ �����

% ����� ��� ���������� ������������� ��������-�������� � "������� ��������"
\RequirePackage{url}

% ����� ��� ���������� ������ ���� ��� � ���������� ������
\RequirePackage{icomma}

% ����� ��� ����������� ������������ �������� ����
\RequirePackage{listings}

% ����� ��� ������������� ������
\RequirePackage{xkeyval}

% ����� ��� ������������ � ����
\RequirePackage[hidelinks]{hyperref}

% ����� ��� ���� �������
\RequirePackage{verbatim}


% 4. ������� �������
\frenchspacing
\doublespacing % �������� "1,5" �� �������

\renewcommand{\rmdefault}{ftm} % ������ ����� �� ������������ --- "Times New Roman" �� ������ pscyr

\newcommand{\setfontsize}[1]{\fontsize{#1pt}{#1pt}\selectfont} % ������� ��� ��������� ������ ������
\newcommand{\invcommas}[1]{\guillemotleft #1\guillemotright} % ������� ��� ����������� ������� �����

% ����� ������������ ���� ���� � ������, �� � �������� �����
\urlstyle{same}

% ����� ������� ��� ������� ������ �������
\fancypagestyle{plain}{
    \fancyhf{}
    \rhead{\thepage}
		\renewcommand{\headrulewidth}{0pt}
		\renewcommand{\footrulewidth}{0pt}
}

% ������� ��� �������� ������� ������ � ���������� ����
\binoppenalty=10000
\relpenalty=10000

% ������� ��� �������� ������������ ����������
\tolerance=1
\emergencystretch=\maxdimen
\hyphenpenalty=10000
\hbadness=10000

% ������� ��� ��������� �������������� ������, ���� ��� �� ����� ���������� � ����
\newcommand{\uchapter}[1]{\chapter*{#1}\addcontentsline{toc}{chapter}{#1}} 

% ��� ��������� ������ ����������� ������� \uchapter
\newcommand{\intro}{\uchapter{�����}}

% ��� ��������� �������� ����������� ������� \uchapter
\newcommand{\conclusions}{\uchapter{��������}}

% ��� ��������� ������� ������� ��������� ����������� ������� \shortings
\newcommand{\shortings}{\uchapter{������ ������� ���������, ��������� � �������}}

% ����� ������� ��� ��������� �������
\newcounter{appendnum}
\newcommand{\append}[1]{
\setcounter{chapter}{0}
\setcounter{figure}{0}
\setcounter{table}{0}
\setcounter{section}{0}
\setcounter{subsection}{0}
\titleformat{\chapter}{\centering\normalsize}{\hspace{1cm}\thechapter}{0.5em}{}
\chapter*{������� \Asbuk{appendnum}\\#1}
\addcontentsline{toc}{chapter}{������� \Asbuk{appendnum}\ #1}
\addvspace{-28pt}
\preto\section{%
	\ifnum\value{section}=0\addvspace{0pt}\fi%
}
\renewcommand{\thefigure}{\Asbuk{appendnum}.\arabic{figure}}
\renewcommand{\thetable}{\Asbuk{appendnum}.\arabic{table}}
\renewcommand{\thesection}{\Asbuk{appendnum}.\arabic{section}}
\renewcommand{\thesubsection}{\Asbuk{appendnum}.\arabic{section}.\arabic{subsection}}
}
% ��������� ���������� ����� � ���������� �������
\pretocmd\append{
	\stepcounter{appendnum}
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
	\ifnum\Asbuk{appendnum}=� \stepcounter{appendnum}\fi
}{}{}

% ������ �������� ���� ���������
% �������� --- ��� ������
\titleformat{\chapter} % �������, �� ���������� ���� �����
			{\centering\normalsize\MakeUppercase} % ������� ������ ����� ("�� �����")
			{\hspace{1cm}\thechapter} % ������� ������ ������ ������: �� ���� ������ �����, ��� ������
			{0.5em} % ������� �� ������� � ������
			{} % �����, �� ������ ����
	
% ����� --- ��� ��������
\titleformat{\section}[block] % �������, �� ���������� ���� �������
			{\normalsize} % ������� ������ ����� (������)
			{\hspace{1.25cm}\thesection} % ������� ������ ������ ������: �� ���� ������ �����, ��� ������
			{0.5em} % ������� �� ������� � ������
			{} % �����, �� ������ ����

% ����� --- ��� �������� �� ������� ����
\titleformat{\subsection}[block] % �������, �� ���������� ���� ������� �������� ����
			{\normalsize} % ������� ������ ����� (������)
			{\hspace{1.25cm}\thesubsection} % ������� ������ ������ ������: �� ���� ������ �����, ��� ������
			{0.5em} % ������� �� ������� � ������
			{} % �����, �� ������ ����
			
% ����� ������ ������� ��� ��������� ������
\titlespacing{\chapter} % �������, �� ���������� ���� �����
			{0pt} % ������ ����
			{-28pt} % ������ ������ (����)
			{48pt} % ������ ����� (2 �����)

% ����� ������ ������� ��� ��������� ��������			
\titlespacing{\section} % �������, �� ���������� ���� �������
			{0pt} % ������ ����
			{48pt} % ������ ������ (2 �����)
			{48pt} % ������ ����� (2 �����)
			
% ����� ������ ������� ��� ��������� ������
\titlespacing{\subsection} % �������, �� ���������� ���� �����
			{0pt} % ������ ����
			{48pt} % ������ ������ (2 �����)
			{48pt} % ������ ����� (2 �����)

% ����� ������� ���, ��� �� ����� ����������� ���� �������� �������
\preto\section{%
	\ifnum\value{section}=0\addvspace{-48pt}\fi%
}

\preto\subsection{%
	\ifnum\value{subsection}=0\addvspace{-48pt}\fi%
}
			
% ����������� ����
\makeatletter
\renewcommand{\tableofcontents}{
	\clearpage
	\thispagestyle{plain}

	\begin{center}
	  \MakeUppercase{����}
	\end{center}
	
	\addvspace{42pt}
	
	\@starttoc{toc}
}
\makeatother

% ������� ������ ��������� ������
\renewcommand{\theequation}{\arabic{chapter}.\arabic{equation}}

% ������ �������� ������, � ����������� ���������
% ����������� ������� ����
\AddEnumerateCounter{\asbuk}{\@asbuk}{\cyrm}
\setlist[itemize,1]{label=-, partopsep=0pt, parsep=0pt, topsep=0pt, itemsep=0pt, itemindent=1.7cm, leftmargin=0pt}
\setlist[itemize,2]{label=-, partopsep=0pt, parsep=0pt, topsep=0pt, itemsep=0pt, itemindent=2.25cm, leftmargin=0pt}
\setlist[enumerate,1]{label=\asbuk*), partopsep=0pt, parsep=0pt, topsep=0pt, itemsep=0pt, itemindent=1.9cm, leftmargin=0pt}
\setlist[enumerate,2]{label=\arabic*), partopsep=0pt, parsep=0pt, topsep=0pt, itemsep=0pt, itemindent=2.6cm, leftmargin=0pt}

% ����� ��������� ������
% ������ ������� �� �������
\renewcommand{\cftchapdotsep}{1}
\renewcommand{\cftsecdotsep}{1}
\renewcommand{\cftsubsecdotsep}{1}

% ������ ����� ����, �� ���������� �� ����� �������
\cftsetpnumwidth{1em}

% ������ ������� �� ������� � ����
\setlength\cftbeforechapskip{0pt}

% ��������� ��������
\renewcommand{\cftchapaftersnum}{} % �� ���� �������� ���� ������ ������ (������)
\renewcommand{\cftchapindent}{0cm} % ������ ������ ������ �� ����� ����
\renewcommand{\cftchapnumwidth}{1em} % ����� ����, �� ���������� �� ����� ������
\renewcommand{\cftchappagefont}{\mdseries} % ����� ������ ������� (���������, 14pt)
\renewcommand{\cftchapfont}{\mdseries} % ����� ��������� (���������)
\renewcommand{\cftchapleader}{\cftdotfill{\cftchapdotsep}} % ��� ����������� ������� �� ��������� �� ������ ������� (�������)

% ����� ��������� ����������
\renewcommand{\cftsecaftersnum}{} % �� ���� �������� ���� ������ �������� (������)
\renewcommand{\cftsecindent}{1em} % ������ ������ �������� �� ����� ����
\renewcommand{\cftsecnumwidth}{2em} % ����� ����, �� ���������� �� ����� ��������
\renewcommand{\cftsecpagefont}{\mdseries} % ����� ������ ������� (���������, 14pt)
\renewcommand{\cftsecfont}{\mdseries} % ����� ��������� (���������)
\renewcommand{\cftsecleader}{\cftdotfill{\cftsecdotsep}} % ��� ����������� ������� �� ��������� �� ������ ������� (�������)

% ����� ��������� ��������
\renewcommand{\cftsubsecaftersnum}{} % �� ���� �������� ���� ������ ������ (������)
\renewcommand{\cftsubsecindent}{3em} % ������ ������ ������ �� ����� ����
\renewcommand{\cftsubsecnumwidth}{2.5em} % ����� ����, �� ���������� �� ����� ������
\renewcommand{\cftsubsecpagefont}{\mdseries} % ����� ������ ������� (���������, 14pt)
\renewcommand{\cftsubsecfont}{\mdseries} % ����� ��������� (���������)
\renewcommand{\cftsubsecleader}{\cftdotfill{\cftsubsecdotsep}} % ��� ����������� ������� �� ��������� �� ������ ������� (�������)

% ��������� �������, ������� � �������
\DeclareCaptionLabelFormat{tablecap}{������� #2} % ������ �� ������������ "����." �� ��������
\DeclareCaptionLabelFormat{figurecap}{������� #2} % ������ �� ������������ "���." �� ��������
\DeclareCaptionFormat{listing}{˳����� ����� #3} % ������ �� ������������ "Listing" �� ��������

\captionsetup[table]{margin=0pt,singlelinecheck=false, justification=justified, labelsep=endash, labelformat=tablecap, font = {stretch = 1.5}, belowskip=18pt, aboveskip=3pt} % ������ ��� �������
\captionsetup[figure]{justification=centering, labelsep=endash, labelformat=figurecap, font = {stretch = 1.5}} % ������ ��� �������
\captionsetup[lstlisting]{margin=0pt, format=listing, singlelinecheck=false, font = {stretch = 1.5}} % ������ ��� �������

\setlength{\textfloatsep}{21pt}
\setlength{\intextsep}{21pt}

% �������, �� ����� �������� ����� �� �������� � ����������
\renewcommand{\thesubfigure}{\asbuk{subfigure}}

% ���� �������� ��� ������ �������
\renewenvironment{table}[4]{
	\begingroup\centering
	\setlength{\LTpre}{-14pt}
  \setlength{\LTpost}{14pt}
  \setlength{\LTcapwidth}{0pt}
  \begin{longtable}{#1}
		\kill
		\caption{#2}\label{#3}\\
		#4
		\endfirsthead
		\kill
		\caption*{����������� ������� \thetable}\\
		#4
		\endhead
		\hline
		\endfoot
}
	{%
	\end{longtable}
	\endgroup	
}

% �������� ������� �� ��������� � ����������
\patchcmd{\thebibliography}
  {\advance\leftmargin\labelsep}
  {\leftmargin=0pt\itemindent=1.9cm\advance\itemindent\labelsep}
  {}{}

% ������� ������ ������ ��� ������� �������� (����� + ������)
\makeatletter
\renewcommand{\@biblabel}[1]{#1.}
\makeatother

% ������� ���������� ��������, ������� ������� ������ ������ �������� � ����
\let\tempbib\thebibliography
\let\tempbibend\endthebibliography
\renewenvironment{thebibliography}{
	\renewcommand{\bibname}{����˲� ��������}% ������� ���������
	\tempbib{99.}% ����������� �������� ����� ������� --- 99
	% ��� �������� ������� �� ���������
	\setlength\partopsep{0pt}
	\setlength\parskip{0pt}
	\setlength\parsep{0pt}
	\setlength\topsep{0pt}
	\setlength\itemsep{0pt}
	\addcontentsline{toc}{chapter}{������ ��������}% ������ � ����
	}
	{
	\tempbibend
}

% ���������� ������� ��� ������� �������
\newcommand{\listing}[2]{\singlespacing\lstinputlisting[language=C++, basicstyle=\tiny, breaklines=true, caption={#1}]{#2}\doublespacing}

% ��� ������� ��� ��������
% ����� ������
\newcommand{\abstractUkr}{\chapter*{�����ֲ�}\thispagestyle{empty}\renewcommand{\arraystretch}{1.5}\setfontsize{14}}
\newcommand{\abstractEng}{\chapter*{ABSTRACT}\thispagestyle{empty}\renewcommand{\arraystretch}{1.5}\setfontsize{14}}

% ���� ������� ��� ���������� ������
% \maketitlepage{params}, �� params --- �� �������� ������ ���� "��������={��������}"
% StudentName --- �������, �������� ��������
% StudentMale --- ����� �������� (true, ���� ������, false --- ���� ����)
% StudentGroup --- ����� ��������
% Title --- ����� ��������� (��� �����)
% SupervisorDegree --- �������� ������, ����� ������ �������� ������
% SupervisorName --- �������, �������� �������� ������
\makeatletter
\define@cmdkey[Work]{Title}{StudentName}{}
\define@boolkey[Work]{Title}{StudentMale}{}
\define@cmdkey[Work]{Title}{StudentGroup}{}
\define@cmdkey[Work]{Title}{Title}{}
\define@cmdkey[Work]{Title}{SupervisorDegree}{}
\define@cmdkey[Work]{Title}{SupervisorName}{}
\newcommand{\maketitlepage}[1]{
	  \setkeys[Work]{Title}{#1}
	  \thispagestyle{empty}
	  \setlength{\parindent}{0cm}
		\begingroup\centering % �����������
			\setfontsize{14}
			\MakeUppercase{������������ ��������� ����������� ������}
			
			\MakeUppercase{\guillemotleft �������� ������������ ��������}
			
			\MakeUppercase{����� ����� ѳ���������\guillemotright}

			��������� ��������� ����������
			
			������� ��������� ����������
		
		\vfill
			
		\cmdWork@Title@Title
		
		\endgroup
		\vfill
		
		\ifWork@Title@StudentMale
			�������:
		\else
			��������:
		\fi \hfill �������:
		
		\ifWork@Title@StudentMale
			�������
		\else
			���������
		\fi ����� \cmdWork@Title@StudentGroup  \hfill 
		\ifundef{\cmdWork@Title@SupervisorDegree}{\relax}%
				{\cmdWork@Title@SupervisorDegree}
				
	 	\cmdWork@Title@StudentName \hfill 	\cmdWork@Title@SupervisorName
		
		\vfill
		
		\begingroup\centering
			��� --- \the\year
			
		\endgroup
		
		\clearpage % �������� � ���� �������

		\setcounter{page}{2} % ����� ������� ���� 2

		\pagestyle{plain}

		\setlength{\parindent}{1.25cm} % ������ ������ ������� ����� ������ (5 �����, ��� 1,25 ��)
		
		% ������� ����� �� �� ���� �������
		\setlength{\belowdisplayskip}{21pt}
		\setlength{\abovedisplayskip}{21pt}
		\setlength{\belowdisplayshortskip}{21pt}
		\setlength{\abovedisplayshortskip}{21pt}
}
\makeatother

% ����������� ������� � ����������� � ��������
\makeatletter
\def\latex@@rquote{^\bgroup\prim@s} 
\let\hang@@h@ngrquote\h@ngrquote
\renewcommand{\h@ngrquote}{
	\relax\ifmmode
		\expandafter\latex@@rquote
	\else
		\expandafter\hang@@h@ngrquote
	\fi}
\makeatother