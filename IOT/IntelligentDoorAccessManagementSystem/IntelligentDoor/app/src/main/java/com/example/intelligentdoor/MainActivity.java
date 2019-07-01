package com.example.intelligentdoor;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.iid.FirebaseInstanceId;
import com.squareup.picasso.Picasso;

public class MainActivity extends AppCompatActivity {
    FirebaseDatabase database;
    DatabaseReference myRef,myRef2,myRef3;
    ImageView im;
    Button b1,b2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        b1=(Button)findViewById(R.id.button2);
        b2=(Button)findViewById(R.id.button3);
        im=(ImageView)findViewById(R.id.imageView2);
        String tkn = FirebaseInstanceId.getInstance().getToken();
        Log.e("Not","Token ["+tkn+"]");

        // Write a message to the database
         database = FirebaseDatabase.getInstance();
         myRef = database.getReference("url");
         myRef2 = database.getReference("command");
         myRef3 = database.getReference("Token");
         myRef3.setValue(tkn);


         b1.setOnClickListener(new View.OnClickListener() {
             @Override
             public void onClick(View view) {
                 myRef2.setValue("1");
             }
         });

         b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                myRef2.setValue("0");
            }
        });

       // myRef.setValue("Hello, World!");

        // Read from the database
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = dataSnapshot.getValue(String.class);
                Log.d("Message", "Value is: " + value);
                Picasso.get().load(value).into(im);


            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w("Message", "Failed to read value.", error.toException());
            }
        });
    }


}

