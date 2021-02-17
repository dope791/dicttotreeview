import git
import sys, os
from slugify import slugify

CI_PROJECT_URL = os.environ.get('CI_PROJECT_URL')

def export_git_remote_info_to_rst(out='./auto',rootdir='../../'):
    
    repo = git.Repo(rootdir)
    remote_refs = repo.remote().refs
    remote_tags = sorted(repo.tags, key=lambda t: t.commit.committed_date)

    with open(out+'/git_remote_info.rst', 'w') as f:
        sys.stdout = f

        print('.. csv-table:: **Git remote branches** ')
        print(' :widths: auto ')
        print(' :header: "branch", "gitlab-doc" \n')

        for refs in remote_refs:
            refname = refs.name
            branch = refname.split('/')[1] 
            if branch != "HEAD":
                print(' "{}", "{}"'.format("`{} <{}/-/tree/{}>`_".format(branch,CI_PROJECT_URL,branch), 
                                                 #"documentation"
                                                 "https://gitlab-doc.baumernet.org/dicttotreeview/"+slugify(branch)
                                                 ))

        print('\n\n')
        print('----')
        print('\n\n')
        print('.. csv-table:: **Git remote tags** ')
        print(' :widths: auto ')
        print(' :header: "tag", "gitlab-doc"\n')

        for tag in remote_tags:
            tagname = tag.name
            #branch = refname.split('/')[1]
            #if branch != "HEAD":
            print(' "{}", "{}"'.format("`{} <{}/-/tree/{}>`_".format(tagname,CI_PROJECT_URL,tagname), 
                                                 #"documentation"
                                                 "https://gitlab-doc.baumernet.org/dicttotreeview/"+slugify(tagname)
                                                 ))

if __name__ == "__main__":
    export_git_remote_info_to_rst()