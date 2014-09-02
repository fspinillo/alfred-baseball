from datetime import datetime, timedelta
import sys
from workflow import Workflow, ICON_WEB, web

def main(wf):
    now = datetime.now()
    baseball_url = "http://gd2.mlb.com/components/game/mlb/year_%d/month_%s/day_%s/master_scoreboard.json" \
                % (now.year, now.strftime("%m"), now.strftime("%d"))

    r = web.get(baseball_url)

    result = r.json()
    posts = result['data']['games']['game']

    if len(wf.args):
        query = wf.args[0]

        query = query.upper()

    for game in posts:
        if (game['home_name_abbrev']) == query or (game['away_name_abbrev']) == query:
            if game['status']['status'] == "In Progress":
                wf.add_item(title='%s (%s) vs %s (%s) @ %s %s' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status']),
                subtitle='B: %s || P: %s || S: %s B: %s O: %s' % (
                game['batter']['name_display_roster'],
                game['pitcher']['name_display_roster'],
                game['status']['s'],
                game['status']['b'],
                game['status']['o'])
            )
            elif (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
                wf.add_item(title='%s (%s) vs %s (%s) @ %s %s' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status']),
                subtitle='W: %s || L: %s || SV: %s' % (
                game['winning_pitcher']['name_display_roster'],
                game['losing_pitcher']['name_display_roster'],
                game['save_pitcher']['name_display_roster'])
                )
            elif (game['status']['status'] == "Pre-Game" or game['status']['status'] == "Preview"):
                wf.add_item(title='%s vs %s @ %s %s%s %s' % (
                game['away_team_name'],
                game['home_team_name'],
                game['venue'],
                game['home_time'],
                game['hm_lg_ampm'],
                game['status']['status']),
                subtitle='P: %s || P: %s' % (
                game['away_probable_pitcher']['name_display_roster'],
                game['home_probable_pitcher']['name_display_roster']))

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))