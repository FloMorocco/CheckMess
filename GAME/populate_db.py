from app import db, Spell

db.create_all()

spell1 = Spell(name='Spell 1', duration=3, target_type='pawn')
spell2 = Spell(name='Spell 2', duration=2, target_type='any')

db.session.add(spell1)
db.session.add(spell2)
db.session.commit()
