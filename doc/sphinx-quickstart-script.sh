#!/bin/bash -e


if [ -z "$plantuml_jar" ]
then
   echo -e "-j option not specified: using default location /app/plantuml.jar for plantuml in Docker container \n"
   plantuml_jar="/app/plantuml.jar"
fi

echo -e "Cleaning artifacts ...\n"
source clean.sh || true


helpFunction()
{
   echo ""
   echo "Usage: $0 -a <author> -v <version> -p <project> -j <location of plantuml.jar>"
   echo -e "\t-p PROJECT"
   echo -e "\t-a AUTHOR"
   echo -e "\t-v VERSION"
   echo -e "\t-j location of your plantuml.jar file"
   exit 1 # Exit script after printing help
}

while getopts "a:v:p:j:" opt
do
   case "$opt" in
      a ) author="$OPTARG" ;;
      v ) version="$OPTARG" ;;
      p ) project="$OPTARG" ;;
      j ) plantuml_jar="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$author" ] || [ -z "$version" ] || [ -z "$project" ] 
then
   echo -e "Some or all of the parameters are empty";
   helpFunction
fi

release=$version
language=en
project_url=$CI_PROJECT_URL
branch=$CI_COMMIT_REF_NAME


echo -e "Using doc/source/Content.rst as master document ...\n"
#\cp doc/source/Content.rst doc/templates/master_doc.rst_t
\cp ../README.rst source/DictToTreeView.rst


echo -e "Running sphinx-quickstart ...\n"

sphinx-quickstart \
    -p $project \
    -a $author \
    -v $version \
    -r $release \
    -l $language \
    -t templates \
    --no-sep \
    --extensions=sphinx_rtd_theme,sphinxcontrib.plantuml \
    -d html_theme=sphinx_rtd_theme \
    -d project_name=$project \
    -d author=$author \
    -d plantuml_jar=$plantuml_jar \
    -d project_url=$project_url \
    -d branch=$branch \


[ -d "source/test_results" ] || mkdir "source/test_results" && echo -e "Creating source/test_results "
[ -f ../test/results.xml ] && cp ../test/results.xml source/test_results || echo "../test/results.xml is not found"
[ -f ../test/time_results.xml ] && cp ../test/time_results.xml source/test_results || echo "../test/time_results.xml is not found"

echo -e "make html ..."
make html

#RemovedInSphinx40Warning, app.add_stylesheet()
echo "No worry about 'RemovedInSphinx40Warning', see https://www.sphinx-doc.org/en/master/extdev/deprecated.html"
