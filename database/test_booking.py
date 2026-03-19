import bcrypt
from database import SessionLocal, engine, Base
from models import User, VM, Node, Booking
from datetime import datetime, time

# Setup
Base.metadata.create_all(bind=engine)
db = SessionLocal()

def hash_password(password: str) -> str:
  
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8') # Spara som sträng i db

def run_test():
    try:
        # 1. Skapa användaren u123456
        user = db.query(User).filter(User.username == "u123456").first()
        if not user:
            hashed_pw = hash_password("password123")
            user = User(username="u123456", hashed_password=hashed_pw)
            db.add(user)
            db.flush()
            print(f"Användare {user.username} skapad.")
        
        # 2. Skapa VM vref1
        vm = db.query(VM).filter(VM.name == "vref1").first()
        if not vm:
            vm = VM(name="vref1")
            db.add(vm)
            db.flush()
            print(f"VM {vm.name} skapad.")
        
        # 3. Skapa noden server1
        node = db.query(Node).filter(Node.name == "server3", Node.vm_id == vm.id).first()
        if not node:
            node = Node(name="server3", vm_id=vm.id)
            db.add(node)
            db.flush()
            print(f"Node {node.name} skapad.")

        # 4. Skapa bokningen: 10:00 - 12:00 idag
        today = datetime.now().date()
        start_dt = datetime.combine(today, time(10, 0))
        end_dt = datetime.combine(today, time(12, 0))

        #  Kollar om bokningen redan finns så det inte skapas dubbletter
        existing_booking = db.query(Booking).filter(
            Booking.vm_id == vm.id, 
            Booking.node_id == node.id,
            Booking.start_time == start_dt
        ).first()

        if not existing_booking:
            new_booking = Booking(
                user_id=user.id,
                vm_id=vm.id,
                node_id=node.id,
                start_time=start_dt,
                end_time=end_dt
            )
            db.add(new_booking)
            db.commit()
            print(f"Bokning lyckades för {vm.name} ({node.name})!")
        else:
            print("Bokningen fanns redan i databasen.")

    except Exception as e:
        db.rollback()
        print(f"Ett fel uppstod: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_test()