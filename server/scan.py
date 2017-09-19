import asyncio
from dateutil.parser import parse
from server import db
from server.models import IssueState, IssueChangeLog
from server.lib import AtLib

LIMIT = 50


def scan(domain, project):
    lib = AtLib(domain)
    loop = asyncio.get_event_loop()
    q = asyncio.Queue(loop=loop)
    producer = fetch_page(lib, project, q)
    consumer = process_changelog(q)

    loop.run_until_complete(asyncio.gather(producer, consumer))
    loop.close()


async def fetch_page(lib, project, q, start=0):
    result = lib.issues_in_project(project, start)
    if result.get('values'):
        await q.put_nowait(result['values'])
    await q.put(None)


async def process_changelog(work_queue):
    changelog = await work_queue.get()
    current_changelog = None

    for value in changelog['values']:
        state_change = list(filter(lambda x: x['field'] == 'status', value['items']))
        if state_change:
            created = parse(value['created'])
            if current_changelog:
                # Commit the last changelog with the new changelog's created date as its end date
                current_changelog.end_datetime = created
                db.session.add(current_changelog)
                db.session.commit()
            for item in state_change:
                from_state = IssueState.query.get(int(item['from']))
                to_state = IssueState.query.get(int(item['to']))
                if not from_state:
                    from_state = IssueState(item['from'], item['fromString'])
                    db.session.add(from_state)
                    db.session.commit()
                if not to_state:
                    to_state = IssueState(item['to'], item['toString'])

                # Create the new changelog, reserve committing it until we get the end time
                current_changelog = IssueChangeLog(created, from_state, to_state)

            # Ensure we add the current change log even if its not closed
            db.session.add(current_changelog)
            db.session.commit()
