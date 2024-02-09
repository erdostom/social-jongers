# Overview
A script for seeding mahjong tournament seating. It uses a SAT solver to pair non-repeating opponents, equally distribute wind seating, and minimize intra-club play.

### Further Reading
* [Social Golfer Problem](https://mathworld.wolfram.com/SocialGolferProblem.html)
* [Good Enough Golfers](https://goodenoughgolfers.com/)
* [Kirkman's Schoolgirl Problem](https://mathworld.wolfram.com/KirkmansSchoolgirlProblem.html)
* [Google Or-Tools](https://phaethonprime.wordpress.com/2019/09/04/using-google-or-tools-for-social-golfers/#:~:text=The%20'Social%20Golfers'%20problem%20asks,the%20user%20named%20'mzl)


### Installation
If you have not already, install the following
* Install Python `paru python` or download [here](https://www.python.org/downloads/)
* Install git `paru git` or download [here](https://git-scm.com/downloads)
* Install git LFS `paru git-lfs` or download [here](https://git-lfs.github.com/)
* Setup LFS `git lfs install`

### Setup
1. Clone this repo `git clone https://gitlab.com/florasoft/social-jongers.git`
3. First time setup `source setup.sh`
5. Run program `source run.sh`