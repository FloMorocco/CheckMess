from app import db, Spell

# Create the tables in the database
db.create_all()

# Add spells
spell1 = Spell(name='Steroid', duration=3, target_type='pawn')
spell2 = Spell(name='Tornado', duration=2, target_type='any')
spell3 = Spell(name='Wall', duration=4, target_type='empty')

# Add spells to the session
db.session.add(spell1)
db.session.add(spell2)
db.session.add(spell3)

# Commit the session to write the changes to the database
db.session.commit()
