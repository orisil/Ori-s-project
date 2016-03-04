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
        private bool button1_was_clicked = false;
        private bool button2_was_clicked = false;
        private bool button3_was_clicked = false;
        private bool button4_was_clicked = false;

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
                textBox3.Hide();
                button4.Hide();

            }

        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {

            if (radioButton2.Checked)
            {
             
                tabPage1.Controls.Add(textBox3);
                tabPage1.Controls.Add(button4);

                textBox3.Show();
                button4.Show();



            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            button1_was_clicked = true;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            button2_was_clicked = true;
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }


        private void button3_Click(object sender, EventArgs e)
        {
            button3_was_clicked = true;
        }

        private void button4_Click(object sender, EventArgs e)
        {
            button3_was_clicked = true;
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        
    }
}
