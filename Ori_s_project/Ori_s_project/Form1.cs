using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Ori_s_project
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

        }


        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void tabPage2_Click(object sender, EventArgs e)
        {

        }

        private void tabPage3_Click(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                textBox1.Hide();
                button1.Hide();

            }

        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {

            if (radioButton2.Checked)
            {
                textBox1 = new System.Windows.Forms.TextBox();

                this.textBox1.Location = new System.Drawing.Point(25, 150);
                this.textBox1.Name = "textBox1";
                this.textBox1.Size = new System.Drawing.Size(100, 20);
                this.textBox1.TabIndex = 1;
                this.textBox1.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
                tabPage1.Controls.Add(textBox1);

                button1 = new System.Windows.Forms.Button();
                this.button1.Location = new System.Drawing.Point(135, 148);
                this.button1.Name = "button1";
                this.button1.Size = new System.Drawing.Size(70, 23);
                this.button1.TabIndex = 4;
                this.button1.Text = "Choose";
                this.button1.UseVisualStyleBackColor = true;
                this.button1.Click += new System.EventHandler(this.button2_Click);
                tabPage1.Controls.Add(button1);


            }

        }

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }


        private void button3_Click(object sender, EventArgs e)
        {

        }



        
    }
}
