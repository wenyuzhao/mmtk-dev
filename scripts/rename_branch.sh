set -ex

old_name=$1
new_name=$2

remote=wenyu

git fetch $remote
git checkout $old_name --force
git pull

# Rename the local branch to the new name
git branch -m $old_name $new_name

# Delete the old branch on remote - where <remote> is, for example, origin
git push $remote --delete $old_name

# Prevent git from using the old name when pushing in the next step.
# Otherwise, git will use the old upstream name instead of <new_name>.
git branch --unset-upstream $new_name

# Push the new branch to remote
git push $remote $new_name

# Reset the upstream branch for the new_name local branch
git push $remote -u $new_name
